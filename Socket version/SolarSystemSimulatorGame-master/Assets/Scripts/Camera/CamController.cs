using UnityEngine;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Collections.Generic; 
using System.Linq; 

[AddComponentMenu("Camera-Control/Space RTS Camera Style")]
public class CamController : MonoBehaviour
{
	public Transform lockedTransform { get; private set; }

	public float xSpeed = 130.0f;
	public float ySpeed = 130.0f;
	public float yMinLimit = -80;
	public float yMaxLimit = 80;
	public float zoomRate = 40;
	public bool panMode = false;
	public float panSpeed = 0.3f;
	public int panThres = 5;
	public float rotationDampening = 5.0f;
	private Transform targetRotation;
	private float xDeg = 0.0f;
	private float yDeg = 0.0f;
	private Vector3 desiredPosition;
	private Vector3 CamPlanePoint;
	private Vector3 vectorPoint;
	private float lastClickTime = 0;
	private float catchTime = 0.25f;
	private bool isLocked = false;
	private Ray ray;
	private Vector3 off = Vector3.zero;
	private Vector3 offSet;
	private Mode mode = Mode.isIdle;
	private enum Mode
	{
		isIdle,
		isRotating,
		isZooming,
		isPanning
	}
	;

	private Thread receiveThread;
	private UdpClient udpClient;
	private int port = 5005; // Choose a port number
	private bool running = true;

	private IPEndPoint lastClientEndpoint;
	private bool isConnected = false;

    private List<Transform> lockableObjects = new List<Transform>();
    private int currentLockIndex = -1;

	private int initial = 0;

    void Awake()
	{
		Init();
	}

	public void Init()
	{
		targetRotation = new GameObject("Cam targetRotation").transform;

		xDeg = Vector3.Angle(Vector3.right, transform.right);
		yDeg = Vector3.Angle(Vector3.up, transform.up);

		LinePlaneIntersect(transform.forward.normalized, transform.position, Vector3.up, Vector2.zero, ref CamPlanePoint);

		targetRotation.position = CamPlanePoint;
		targetRotation.rotation = transform.rotation;

		lockedTransform = null;
	}

	void Start()
	{
		InitNetwork();
		Debug.Log("Camera controller initialized. Waiting for Python connection...");

        lockableObjects = new List<Transform>(Planet.planetList.Select(p => p.transform));
        if (lockableObjects.Count > 0)
        {
            int randomIndex = Random.Range(0, lockableObjects.Count);
            LockObject(lockableObjects[randomIndex]);
        }

    }

	private void InitNetwork()
	{
		receiveThread = new Thread(new ThreadStart(ReceiveData));
		receiveThread.IsBackground = true;
		receiveThread.Start();
	}

	private void ReceiveData()
	{
		try
		{
			udpClient = new UdpClient(port);
			Debug.Log("UDP server started on port " + port);

			while (running)
			{
				try
				{
					IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
					byte[] data = udpClient.Receive(ref anyIP);

					// Get the dispatcher instance once at start
					var dispatcher = UnityMainThreadDispatcher.Instance;
					if (dispatcher == null)
					{
						Debug.LogError("Dispatcher not available - skipping message");
						continue;
					}

					string message = Encoding.UTF8.GetString(data);

					// Handle connection state
					if (lastClientEndpoint == null || !lastClientEndpoint.Equals(anyIP))
					{
						lastClientEndpoint = anyIP;
						UnityMainThreadDispatcher.Enqueue(() =>
						{
							Debug.Log($"Python client connected: {anyIP.Address}:{anyIP.Port}");
						});
					}

					// Process command
					UnityMainThreadDispatcher.Enqueue(() => ProcessCommand(message));
				}
				catch (SocketException e)
				{
					if (lastClientEndpoint != null)
					{
						lastClientEndpoint = null;
						UnityMainThreadDispatcher.Enqueue(() =>
						{
							Debug.LogWarning("Python client disconnected");
						});
					}
				}
				catch (System.Exception e)
				{
					UnityMainThreadDispatcher.Enqueue(() =>
					{
						Debug.LogError($"Network error: {e.Message}");
					});
				}
			}
		}
		finally
		{
			udpClient?.Close();
			Debug.Log("UDP server stopped");
		}
	}

	void OnDestroy()
	{
		running = false;
	}

    private void CycleLockTarget()
    {
        if (lockableObjects.Count == 0) return;

        currentLockIndex = (currentLockIndex + 1) % lockableObjects.Count;
        LockObject(lockableObjects[currentLockIndex]);
        Debug.Log($"Locked to: {lockableObjects[currentLockIndex].name}");
    }

    private void ProcessCommand(string command)
	{
		// Parse the command from Python
		string[] parts = command.Split(' ');

		if (parts.Length < 1) return;

		switch (parts[0])
		{
            case "ROTATE_UP":
                yDeg -= ySpeed * 0.5f; // Small incremental change
                yDeg = ClampAngle(yDeg, yMinLimit, yMaxLimit, 5);
                mode = Mode.isRotating;
                break;

            case "ROTATE_DOWN":
                yDeg += ySpeed * 0.5f;
                yDeg = ClampAngle(yDeg, yMinLimit, yMaxLimit, 5);
                mode = Mode.isRotating;
                break;

            case "ROTATE_LEFT":
                xDeg -= xSpeed * 0.5f;
                mode = Mode.isRotating;
                break;

            case "ROTATE_RIGHT":
                xDeg += xSpeed * 0.5f;
                mode = Mode.isRotating;
                break;

            // Existing commands
            case "ZOOM":
                if (parts.Length == 2)
                {
                    float amount = -0.7f * float.Parse(parts[1]);
                    desiredPosition = (-(targetRotation.position - transform.position) * amount + transform.position);
                    mode = Mode.isZooming;
                }
                break;

           /* case "PAN":
                if (parts.Length == 3)
                {
                    float x = float.Parse(parts[1]);
                    float y = float.Parse(parts[2]);
                    Vector3 panVector = new Vector3(x, 0, y) * panSpeed;
                    targetRotation.Translate(panVector, Space.World);
                    transform.Translate(panVector, Space.World);
                    mode = Mode.isPanning;
                }
                break;*/

            case "LOCK":
                if (parts.Length == 2)
                {
                    GameObject obj = GameObject.Find(parts[1]);
                    if (obj != null) LockObject(obj.transform);
                }
                break;

			case "UNLOCK":
				UnlockObject();
				break;

            case "NEXT_LOCK":

				if (initial == 0)
					initial = 1;

				else
					CycleLockTarget();

                break;
        }
	}

	void OnApplicationQuit()
	{
		running = false;
		if (udpClient != null)
		{
			udpClient.Close();
		}
		if (receiveThread != null)
		{
			receiveThread.Abort();
		}
		Debug.Log("Camera controller server stopped");
	}

	void LateUpdate()
	{

		if (isLocked)
		{
            offSet = lockedTransform.position - off;
            off = lockedTransform.position;

            float magnitude = (targetRotation.position - transform.position).magnitude;
            transform.position = targetRotation.position - (transform.rotation * Vector3.forward * magnitude) + offSet;
            targetRotation.position = targetRotation.position + offSet;
        }

		switch (mode)
		{
			case Mode.isIdle:

				break;

			case Mode.isRotating:

                transform.rotation = Quaternion.Euler(yDeg, xDeg, 0);
                targetRotation.rotation = transform.rotation;

                float magnitude = (targetRotation.position - transform.position).magnitude;
                transform.position = targetRotation.position - (transform.rotation * Vector3.forward * magnitude) + offSet;
                targetRotation.position = targetRotation.position + offSet;
                mode = Mode.isIdle; // Reset mode after processing
                break;

            case Mode.isZooming:

                transform.position = Vector3.Lerp(transform.position, desiredPosition, zoomRate * Time.deltaTime);
                if (Vector3.Distance(transform.position, desiredPosition) < 0.1f)
                {
                    mode = Mode.isIdle;
                }
                break;

            case Mode.isPanning:

				if (panMode == true)
				{
					float panNorm = transform.position.y;
					if ((Input.mousePosition.x - Screen.width + panThres) > 0)
					{
						targetRotation.Translate(Vector3.right * -panSpeed * Time.deltaTime * panNorm);   //here, right is wrt the loc ref because Space.Self by default
						transform.Translate(Vector3.right * -panSpeed * Time.deltaTime * panNorm);
					}
					else if ((Input.mousePosition.x - panThres) < 0)
					{
						targetRotation.Translate(Vector3.right * panSpeed * Time.deltaTime * panNorm);
						transform.Translate(Vector3.right * panSpeed * Time.deltaTime * panNorm);
					}
					if ((Input.mousePosition.y - Screen.height + panThres) > 0)
					{
						vectorPoint.Set(transform.forward.x, 0, transform.forward.z);
						targetRotation.Translate(vectorPoint.normalized * -panSpeed * Time.deltaTime * panNorm, Space.World);
						transform.Translate(vectorPoint.normalized * -panSpeed * Time.deltaTime * panNorm, Space.World);
					}
					if ((Input.mousePosition.y - panThres) < 0)
					{
						vectorPoint.Set(transform.forward.x, 0, transform.forward.z);
						targetRotation.Translate(vectorPoint.normalized * panSpeed * Time.deltaTime * panNorm, Space.World);
						transform.Translate(vectorPoint.normalized * panSpeed * Time.deltaTime * panNorm, Space.World);
					}
				}
				break;

			default:
				break;
		}

		transform.position = Vector3.ClampMagnitude(transform.position, Scales.solarSystemEdge);
	}

	public void LockObject(Transform transformToLock)
	{
		mode = Mode.isIdle;

		isLocked = true;
		lockedTransform = transformToLock;
		off = lockedTransform.position;

		targetRotation.position = lockedTransform.position;
		transform.position = targetRotation.position - new Vector3(1.5f * lockedTransform.localScale.x, -1.5f * lockedTransform.localScale.x, 0);
	}

	private void UnlockObject()
	{
		isLocked = false;
		lockedTransform = null;
		offSet = Vector3.zero;
	}

	private float LinePlaneIntersect(Vector3 u, Vector3 P0, Vector3 N, Vector3 D, ref Vector3 point)
	{
		float s = Vector3.Dot(N, (D - P0)) / Vector3.Dot(N, u);
		point = P0 + s * u;
		return s;
	}

	private static float ClampAngle(float angle, float minOuter, float maxOuter, float inner)
	{
		if (angle < -360)
			angle += 360;
		if (angle > 360)
			angle -= 360;

		angle = Mathf.Clamp(angle, minOuter, maxOuter);

		if (angle < inner && angle > 0)
			angle -= 2 * inner;
		else if (angle > -inner && angle < 0)
			angle += 2 * inner;

		return angle;
	}


}
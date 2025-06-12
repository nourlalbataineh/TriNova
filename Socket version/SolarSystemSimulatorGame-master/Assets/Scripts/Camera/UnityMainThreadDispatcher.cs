using UnityEngine;
using System.Collections.Generic;
using System.Threading;

public class UnityMainThreadDispatcher : MonoBehaviour
{
    private static UnityMainThreadDispatcher _instance;
    private static readonly Queue<System.Action> _executionQueue = new Queue<System.Action>();
    private static readonly object _lock = new object();
    private static bool _applicationIsQuitting = false;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    private static void AutoInitialize()
    {
        // Force initialization when the game starts
        var dummy = Instance;
    }

    public static UnityMainThreadDispatcher Instance
    {
        get
        {
            if (_applicationIsQuitting)
            {
                Debug.LogWarning("Application is quitting - dispatcher unavailable");
                return null;
            }

            lock (_lock)
            {
                if (_instance == null)
                {
                    _instance = FindObjectOfType<UnityMainThreadDispatcher>();
                    if (_instance == null)
                    {
                        GameObject container = new GameObject("UnityMainThreadDispatcher");
                        _instance = container.AddComponent<UnityMainThreadDispatcher>();
                        DontDestroyOnLoad(container);
                        Debug.Log("MainThreadDispatcher initialized");
                    }
                }
                return _instance;
            }
        }
    }

    void Awake()
    {
        lock (_lock)
        {
            if (_instance == null)
            {
                _instance = this;
                DontDestroyOnLoad(gameObject);
            }
            else if (_instance != this)
            {
                Destroy(gameObject);
            }
        }
    }

    void Update()
    {
        lock (_lock)
        {
            while (_executionQueue.Count > 0)
            {
                try
                {
                    _executionQueue.Dequeue()?.Invoke();
                }
                catch (System.Exception e)
                {
                    Debug.LogError($"Error executing queued action: {e}");
                }
            }
        }
    }

    public static void Enqueue(System.Action action)
    {
        if (_applicationIsQuitting || action == null) return;

        lock (_lock)
        {
            _executionQueue.Enqueue(action);
        }
    }

    void OnApplicationQuit()
    {
        _applicationIsQuitting = true;
        lock (_lock)
        {
            _executionQueue.Clear();
            _instance = null;
        }
    }
}
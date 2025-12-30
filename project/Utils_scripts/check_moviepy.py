try:
    import moviepy
    print(f"MoviePy version: {moviepy.__version__}")
    print(f"Dir moviepy: {dir(moviepy)}")
except ImportError as e:
    print(f"Error: {e}")

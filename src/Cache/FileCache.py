import functools
import os
import pickle


def FileCache(filename):
    def decorator_cache(func):
        @functools.wraps(func)
        def wrapper_cache(*args, **kwargs):
            cache_file = f"{filename}.pkl"
            
            # If cache file exists, load the cached data
            if os.path.exists(cache_file):
                with open(cache_file, "rb") as f:
                    cache = pickle.load(f)
            else:
                cache = {}

            # Use a tuple of the function's arguments and keyword arguments as the cache key

            # remove the first argument (self) from the args tuple
            args_only = args[1:]

            cache_key = (args_only, tuple(sorted(kwargs.items())))

            # If the result is not in the cache, call the function and store the result
            if cache_key not in cache:
                result = func(*args, **kwargs)
                cache[cache_key] = result

                # Save the updated cache to the file
                with open(cache_file, "wb") as f:
                    pickle.dump(cache, f)
            else:
                # ask the user if they want to use the cached result
                c = input(f"[CACHE] ({cache_file}) Cache hit, re-run? y/n: ")
                if c != "y":
                    result = func(*args, **kwargs)
                    cache[cache_key] = result

                    # Save the updated cache to the file
                    with open(cache_file, "wb") as f:
                        pickle.dump(cache, f)

            return cache[cache_key]

        return wrapper_cache

    return decorator_cache

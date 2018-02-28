import concurrent.futures


def threaded(fcn):
    def wrapper(*args, **kwargs):
        results = {}
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor() as executor:

            futures = {executor.submit(fcn, [i]): idx for idx,
                       i in enumerate(args[0])}

            tasks = len(futures)
            tenth = round(tasks / 10)
            print('Formed pool of {} tasks'.format(tasks))

            for idx, future in enumerate(concurrent.futures.as_completed(futures)):
                i = futures[future]
                try:
                    # store result
                    data = future.result()
                    # check to see if in array form
                    if len(data) == 1:
                        data = data[0]
                    results[i] = data
                except Exception as exc:
                    print('{} generated an exception: {}'.format(
                        args[0][i], exc))

                if tenth != 0 and idx != 0 and idx % tenth == 0:
                    print('{}% Done'.format((idx // tenth) * 10))

        # sort and put in array
        final = []
        for k, v in sorted(results.items()):
            final.append(v)

        return final
    return wrapper


def execute_task(val):
   # do something threadable
   return val * 10


@threaded
def runner_fcn(values):
   results = []
   for v in values:
       results.append(execute_task(v))
   return results


if __name__ == '__main__':
    res = runner_fcn(list(range(100)))
    print(res)

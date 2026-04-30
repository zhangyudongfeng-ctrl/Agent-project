'''
 * @Author       : MatthewZhang
 * @Date         : 2026-04-29 13:30:54
 * @Description  : 
'''

# 不是写了async就是异步了，而是要把代码里所有需要等待的部分全部替换为async才算是异步操作，async 函数里可以有普通同步代码，但所有可能长时间等待的 IO 操作，都要尽量换成可 await 的异步版本

import asyncio
import time

# 相当于是子函数
async def task(name: str, seconds: int):
    print(f"{name} 开始")
    # await asyncio.sleep(seconds)    # 异步阻塞
    time.sleep(seconds)     # 同步阻塞
    print(f"{name} 结束，耗时 {seconds} s")

# 相当于是主函数， 每个主函数内部运行多个子函数， 用于统一管理子函数
async def main():
    t1 = time.perf_counter()
    await asyncio.gather(
        task('A', 3),
        task('B', 1),
        task('C', 2)
    )
    print(f"total time = {time.perf_counter() - t1} s")

asyncio.run(main=main())
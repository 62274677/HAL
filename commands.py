import pytablewriter as ptw
from multiprocessing import cpu_count
def table_test(client,message):
    writer = ptw.MarkdownTableWriter()
    writer.max_workers = cpu_count()
    
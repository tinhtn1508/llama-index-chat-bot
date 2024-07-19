import crawler
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, default='server', help='server or crawler')
    parser.parse_args()
    args = parser.parse_args()
    if args.type == 'crawler':
        print('Start crawling the llama index blogs...')
        blogs = crawler.list_llama_index_blogs()
        print('There are {} blogs in total'.format(len(blogs)))
        for blog in blogs:
            data = crawler.get_blog_detail(blog['url'])
            crawler.store_blog_detail(blog, data)
        print('Finish crawling the llama index blogs')
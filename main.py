import crawler
import argparse
import embedding
import server

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, default='server', help='server or crawler')
    parser.add_argument('--collection_name', type=str, default='llama_index_blogs', help='collection name')
    parser.add_argument('--embedding_type', type=str, default='google', help='embedding type')
    parser.add_argument('--llm', type=str, default='gemini', help='llm type')
    parser.parse_args()
    args = parser.parse_args()
    if args.type == 'crawler':
        print('Start crawling the llama index blogs...')
        blogs = crawler.list_llama_index_blogs()
        print('There are {} blogs in total'.format(len(blogs)))
        for blog in blogs:
            text = crawler.get_blog_detail(blog['url'], 'text')
            markdown = crawler.get_blog_detail(blog['url'], 'markdown')
            crawler.store_blog_detail(blog, text, markdown)
        print('Finish crawling the llama index blogs')
    elif args.type == 'embedding':
        print('Start loading the embedding...')
        embedding.load_embedding(documents_directory='data', collection_name=args.collection_name, persist_directory='chroma_storage', embedding_type=args.embedding_type)
        print('Finish loading the embedding')
    else:
        server.server(collection_name='llama_index_blogs', persist_directory='chroma_storage', embedding_type='google', llm=args.llm)
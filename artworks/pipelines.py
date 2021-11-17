class ArtworksPipeline:
    def process_item(self, item, spider):
        #There is no concrete tag containning the title (meanind the tag with id "title"),
        # and the title taken from <head> contains authors. Regexp removing authors from head title is not perfect
        #and might remove some valid part of the title, so as some form of a check i make a decision on where to take
        #the title from based on their lenghts
        if 'head_title' in item and 'title' in item:
            if len(item['head_title']) <= len(item['title']):
                del item['head_title']
            else:
                item['title'] = item['head_title']
                del item['head_title']
        elif 'head_title' in item and 'title' not in item:
            item['title'] = item['head_title']
            del item['head_title']
        return item

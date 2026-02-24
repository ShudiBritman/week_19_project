def build_index_schema(image_details, topic):
    to_index = {
        "id": image_details['id'],
        "meta_data" : image_details['meta_data'],
        "image_text": {
            topic: image_details['image_text']
        }
    }
    return to_index
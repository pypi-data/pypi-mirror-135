import asyncio
import aiohttp
import pyimgbox




def post(input_records = None):
    """Takes schema record entity and load image from path defined at temp:filepath
    Returns new imageobject with contenturl and thumbnailurl
    """

    #loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    input_record = {
        '@id': 'test_id', 
        '@type': 'schema:ImageObject', 
        'temp:filepath': 'image.jpg'
    }

    output_records = loop.run_until_complete(post_async(input_record))

    return output_records

async def post_async(input_records):
    """Takes schema record entity and load image from path defined at temp:filepath
    Returns new imageobject with contenturl and thumbnailurl
    """

    if not isinstance(input_records, list): 
        input_records = [input_records]

    # Write files to site
    tasks = []
    tasks.append(asyncio.ensure_future(post_to_image_sharing(input_records)))
    output_records = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Convert back to non list
    while type(output_records) is list and len(output_records) <= 1:
        output_records = output_records[0]

    return output_records


async def post_to_image_sharing(input_records):


    # Get filepaths from records
    filepaths = []
    for r in input_records:
        filepaths.append(r.get('temp:filepath', None))

    # Load filepaths
    async with pyimgbox.Gallery(title="References", adult = True, square_thumbs = True, thumb_width = 200) as gallery:
        output_records = []
        try:
            async for submission in gallery.add(filepaths):

                record_imageObject = {
                    '@type': 'schema:ImageObject',
                    'schema:thumbnailUrl': submission.thumbnail_url,
                    'schema:contentUrl': submission.image_url
                }
                
                # Find corresponding record id
                for i in input_records:
                    if i.get('temp:filepath', None) == submission.filepath:
                        record_imageObject['@id'] = i.get('@id', None)
                
                output_records.append(record_imageObject)
        except Exception as e:
            print('error', e)

    # Match files uploaded with original record
   

    return output_records

post()


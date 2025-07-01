import xml.etree.ElementTree as ET
import json
from datetime import datetime

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"
ET.register_namespace('itunes', ITUNES_NS)

def create_podcast_xml_from_json(json_path: str, output_path: str):
    with open(json_path, 'r') as f:
        info = json.load(f)

    rss = ET.Element('rss', version='2.0', attrib={
        'xmlns:itunes': ITUNES_NS
    })
    channel = ET.SubElement(rss, 'channel')

    ET.SubElement(channel, 'title').text = info['title']
    ET.SubElement(channel, 'link').text = info['link']
    ET.SubElement(channel, 'description').text = info['description']
    ET.SubElement(channel, 'language').text = info['language']

    ET.SubElement(channel, f'{{{ITUNES_NS}}}author').text = info['author']
    owner = ET.SubElement(channel, f'{{{ITUNES_NS}}}owner')
    ET.SubElement(owner, f'{{{ITUNES_NS}}}name').text = info['owner_name']
    ET.SubElement(owner, f'{{{ITUNES_NS}}}email').text = info['owner_email']
    ET.SubElement(channel, f'{{{ITUNES_NS}}}explicit').text = info.get('explicit', 'no')
    ET.SubElement(channel, f'{{{ITUNES_NS}}}image', href=info['image'])
    ET.SubElement(channel, f'{{{ITUNES_NS}}}category', text=info['category'])

    tree = ET.ElementTree(rss)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

def add_episode_to_xml(xml_path: str, title: str, description: str, media_url: str, 
                       media_length: str, pub_date: str, duration: str, episode: int, season: int, explicit: str):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    channel = root.find('channel')

    new_item = ET.Element('item')
    ET.SubElement(new_item, 'title').text = title
    ET.SubElement(new_item, 'description').text = description
    ET.SubElement(new_item, 'enclosure', {
        'url': media_url,
        'length': media_length,
        'type': 'audio/mpeg'
    })
    ET.SubElement(new_item, 'guid').text = media_url
    ET.SubElement(new_item, 'pubDate').text = pub_date
    ET.SubElement(new_item, f'{{{ITUNES_NS}}}duration').text = duration
    ET.SubElement(new_item, f'{{{ITUNES_NS}}}episode').text = str(episode)
    ET.SubElement(new_item, f'{{{ITUNES_NS}}}season').text = str(season)
    ET.SubElement(new_item, f'{{{ITUNES_NS}}}explicit').text = explicit

    channel.append(new_item)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)
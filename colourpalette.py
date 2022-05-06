'''
Purpose: Create colour palettes from uploaded images
CreatedBy: DBrookes
CreatedOn: 06052022
Notes:
'''
#requirements
import io
import streamlit as st
import math
import pandas as pd
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib import gridspec
import extcolors
import json
st.set_option('deprecation.showPyplotGlobalUse', False)

#Introduction to App
st.title('Colour palette generator')
st.markdown('Use this app to generate colour palettes from a source image\
     for use in your websites, presenations or charts :)')

#Image Import
st.header('Upload an image to generate a colour palette')
raw_img =  st.file_uploader(label='Upload Image', type=['png','jpg'],
help= 'Upload a .png or .jpg less than 200MB in size')
if raw_img is not None:
    img = Image.open(raw_img)
    st.image(image= img, caption='Source Image')

    @st.cache
    #Main Function
    def get_palettes(img):
        colours = extract_colours(img)
        colour_palette = render_colour_palette(colours)
        overlay_palette(img,colour_palette)
        return plt

    def extract_colours(img):
        tolerance = 32
        limit = 12
        colours, pixel_count = extcolors.extract_from_image(img, tolerance,limit)
        return colours

    def render_colour_palette(colours):
        size = 100
        columns = 6
        width = int(min(len(colours),columns)*size)
        height = int((math.floor(len(colours)/columns)+1)*size)
        result = Image.new('RGBA',(width,height),(0,0,0,0))
        canvas = ImageDraw.Draw(result)
        for idx, colour in enumerate(colours):
            x = int((idx % columns)*size)
            y = int(math.floor(idx / columns)*size)
            canvas.rectangle([(x,y), (x + size -1,y + size -1)], fill=colour[0])
        return result

    def overlay_palette(img,colour_palette):
        nrow = 2
        ncol = 1
        f = plt.figure(figsize=(30,30),facecolor='None', edgecolor='k',dpi=100,num=None)
        gs = gridspec.GridSpec(nrow,ncol,wspace=0.0,hspace=0.0)
        f.add_subplot(2,1,1)
        plt.imshow(img,interpolation='nearest')
        plt.axis('off')
        f.add_subplot(1,2,2)
        plt.imshow(colour_palette,interpolation='nearest')
        plt.axis('off')
        plt.subplots_adjust(wspace=0, hspace=0,bottom=0)
        return plt

    with st.container():
        st.header('Colour Palette Results')
        st.pyplot(get_palettes(img))

    def flatten(list_of_lists):
        if len(list_of_lists) == 0:
            return list_of_lists
        if isinstance(list_of_lists[0], list):
            return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
        return list_of_lists[:1] + flatten(list_of_lists[1:])

    with st.container():
        st.header('Colour Palette RGB')
        st.text('[Red,Green,Blue],Count')
        colour_list = json.dumps(extract_colours(img))
        st.write(colour_list)
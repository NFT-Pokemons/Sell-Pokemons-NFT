import streamlit as st
import os
import random
from PIL import Image
#st.title('NFT-Pokemons')

global path
path = 'pokemon-gpt-2-output'
im_list = os.listdir(path)
random_img = random.randint(1, len(im_list))

st.set_page_config(layout="wide")

st.markdown("""
<style>
.big-font {
    font-size:100px !important;
}
.small-font {
    font-size: 50px !important;

}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">NFT-Pokemons</p>', unsafe_allow_html=True)

st.markdown('<p class="small-font">Generate your own image</p>', unsafe_allow_html=True)

def gen_file(size, random_img):
    img = Image.open(path + '/' + im_list[random_img])
    resized_im = img.resize((size, size))
    st.image(resized_im)

# st.write("""
# # Generate your own image
# """)

size = st.sidebar.slider('size', 64, 640)
open_file = st.sidebar.button('GENERATE')
if open_file:
    gen_file(size, random_img)

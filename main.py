import streamlit as st
import os
import random
import urllib3

from PIL import Image
from zora_nft_utils import login_and_mint

urllib3.disable_warnings()

PATH = 'pokemon-gpt-2-output'
im_list = os.listdir(PATH)


def gen_file(size):
    x = random.randint(1, len(im_list))
    img = Image.open('pokemon-gpt-2-output' + '/' + im_list[x])
    resized_im = img.resize((size, size))
    with col2:
        st.image(resized_im)
    with open('rand.txt', "w") as f:
        f.write(str(x))
    return x


st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color: #DA4E4E;font-size:80px;'>Pokemons NFT</h1>",
            unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #DA4E4E; font-size:60px; ' >GENERATE & TAKE PROFIT</p>",
            unsafe_allow_html=True)

default_value_goes_here = ''
size = st.slider('size', 64, 640)
open_file = st.button('GENERATE')

col1, col2, col3 = st.beta_columns(3)


if open_file:
    x = gen_file(size)

st.markdown("<p style='color: #CD0832; font-size:25px; ' >Please, enter your own privatе key</p>",
            unsafe_allow_html=True)
user_input = st.text_input(default_value_goes_here)

token_minter = st.button('Mint NFT!')

if token_minter:
    with open('rand.txt', "r") as f:
        x = int(f.read())
    login_and_mint(user_input, im_list[x])

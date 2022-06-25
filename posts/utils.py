
from django.shortcuts import render, redirect, HttpResponse
from .models import *
import re


ordinal_values = {' ': 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11,
                  'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22,
                  'w': 23, 'x': 24, 'y': 25, 'z': 26}
jew_values = {' ': 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 600, 'k': 10,
              'l': 20, 'm': 30, 'n': 40, 'o': 50, 'p': 60, 'q': 70, 'r': 80, 's': 90, 't': 100, 'u': 200, 'v': 700,
              'w': 900, 'x': 300, 'y': 400, 'z': 500}
pythagorean = {' ': 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 1, 'k': 2,
                  'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9, 's': 1, 't': 2, 'u': 3, 'v': 4,
                  'w': 5, 'x': 6, 'y': 7, 'z': 8}

def initialize():
    Simple, screated = Cipher.objects.get_or_create(name="Simple", color="#1FFF54")
    Sumerian, sumcreated = Cipher.objects.get_or_create(name="Sumerian", color="#FF0000")
    Jewish, jcreated = Cipher.objects.get_or_create(name="Jewish", color="#666999")
    Pythagorean, pcreated = Cipher.objects.get_or_create(name="Pythagorean", color="##D4AF37")

    if screated:
        for key, val in ordinal_values.items():
            Symbol.objects.create(char=key, value=val, cipher="Simple")
            Symbol.objects.create(char=key.upper(), value=val, cipher="Simple")
    if sumcreated:
        for key, val in ordinal_values.items():
            Symbol.objects.create(char=key, value=(val*6), cipher="English")
            Symbol.objects.create(char=key.upper(), value=(val*6), cipher="English")
    if jcreated:
        for c, v in jew_values.items():
            Symbol.objects.create(char=c, value=v, cipher="Jewish")
            Symbol.objects.create(char=c.upper(), value=v, cipher="Jewish")
    if pcreated:
        for c, v in pythagorean.items():
            Symbol.objects.create(char=c, value=v, cipher="Pythagorean")
            Symbol.objects.create(char=c.upper(), value=v, cipher="Pythagorean")

def post_create(cipher, content, author, ip, parent="0"):
    parent = int(parent)
    p_t = " ".join(content.split())
    phrase_text = re.sub("[^a-zA-Z ]", "", p_t)
    if phrase_text[0] == " ":
        phrase_text = phrase_text[1:]

    this_phrase, created = Phrase.objects.get_or_create(text=phrase_text)

    if created:
        vals = []
        for ciph in Cipher.objects.all():
            ciph_val = []
            for s in ciph.symbols:
                for l in phrase_text:
                    if s.char == l:
                        ciph_val.append(s.value)
            
            val = sum(ciph_val)
            g, c = Value.objects.get_or_create(num=val, ciph=ciph)
            this_phrase.values.add(g)
            vals.append(g)

    if parent != 0:
        p_post = Post.objects.get(id=parent)
        if p_post.cipher:
            c_val = 0
            for val in p_post.values.all():
                if val.ciph == p_post.cipher:
                    c_vals = []
                    for s in p_post.cipher.symbols:
                        for l in content:
                            if s.char == l:
                                c_vals.append(s.value)
                    c_val = sum(c_vals)
                    if c_val == val.num:
                        post, made = Post.objects.get_or_create(content=content, author=author, phrase=this_phrase)
                        if made:
                            p_post.replies.add(post)
                            p_post.save()
                            if cipher != "None":
                                post.cipher = Cipher.objects.get(name=cipher)
                            for cip in Cipher.objects.all():
                                hodler = []
                                for sym in cip.symbols:
                                    for let in post.content:
                                        if sym.char == let:
                                            hodler.append(sym.value)
                                tval = sum(hodler)
                                getval, valmade = Value.objects.get_or_create(num=tval, ciph=cip)
                                post.values.add(getval)
                            votes = Vote.objects.create(user=author, value=True, post=post)
                            post.save()
                            return 'Posted'
                    else:
                        return 'Not Equal'
        else:
            post, made = Post.objects.get_or_create(content=content, author=author, phrase=this_phrase)
            if made:
                p_post.replies.add(post)
                p_post.save()
                if cipher != "None":
                    post.cipher = Cipher.objects.get(name=cipher)
                for cip in Cipher.objects.all():
                    hodler = []
                    for sym in cip.symbols:
                        for let in post.content:
                            if sym.char == let:
                                hodler.append(sym.value)
                    tval = sum(hodler)
                    getval, valmade = Value.objects.get_or_create(num=tval, ciph=cip)
                    post.values.add(getval)
                votes = Vote.objects.create(user=author, value=True, post=post)
                post.save()
                return 'Posted'
    else:
        post, made = Post.objects.get_or_create(content=content, author=author, phrase=this_phrase)
        if made:
            if cipher != "None":
                post.cipher = Cipher.objects.get(name=cipher)
            for cip in Cipher.objects.all():
                hodler = []
                for sym in cip.symbols:
                    for let in post.content:
                        if sym.char == let:
                            hodler.append(sym.value)
                tval = sum(hodler)
                getval, valmade = Value.objects.get_or_create(num=tval, ciph=cip)
                post.values.add(getval)
            votes = Vote.objects.create(user=author, value=True, post=post)
            post.save()
            return 'Posted'
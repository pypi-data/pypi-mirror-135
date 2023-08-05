pypoh
=====

A Python Wrapper for the Proof of Humanity Rest API.

Overview
========

With pypoh you can easily access all the information available at
https://app.proofofhumanity.id/ and integrate it in you apps and/or Data
Analysis tools.

-  Check if an ETH address has a registered profile at POH.
-  Download a list of Humans with all their data (registry history,
   given vouches, received vouches, name, photo link, etc).
-  Use the built-in **Human()** class to manage this data faster.

How to use it
=============

Import
------

You can easily import pypoh with:

.. code:: python:

   import pypoh

Or import only the methods you need with:

.. code:: python:

   from pypoh import Human, ping, get_list_of_humans

Human Class Usage
-----------------

pypoh comes with a class called “Human” that has all the data for a
single real human registered at Proof of Humanity.

.. code:: python:

   human = Human(address="0xSOME_ETH_ADDRESS")

Some Class Methods:
~~~~~~~~~~~~~~~~~~~

.. code:: python:

   print(human.get_status_history)

..

   { “status”: “VOUCHING”, “time”: “2022-01-11T01:13:06.790Z” }

.. code:: python:

   print(human.get_given_vouches)

..

   { “eth_address”: “0xf49a19f72d0e106df462cfd6b5bebe42b6001616”,
   “status”: “VOUCHING”, “vanity_id”: 1, “display_name”: “satoshin”,
   “first_name”: “Satoshi”, “last_name”: “Nakamoto”, “registered”: true,
   “photo”:
   “https://ipfs.kleros.io/ipfs/QmXmLgii8brfAP7edaabbRHey5VKvFhqqpSFfJf4sD1Lf6/image.jpg”,
   “video”:
   “https://ipfs.kleros.io/ipfs/QmXmLgii8brfAP7edaabbRHey5VKvFhqqpSFfJf4sD1Lf6/video.mp4”,
   “bio”: “Chancellor on brink of second bailout for banks.”, “profile”:
   “https://app.proofofhumanity.id/profile/0xf49a19f72d0e106df462cfd6b5bebe42b6001615”,
   “registered_time”: “2022-01-11T01:11:25.486Z”, “creation_time”:
   “2022-01-11T01:11:25.486Z” }

.. code:: python:

   print(human.get_received_vouches)

..

   { “eth_address”: “0xf49a19f72d0e106df462cfd6b5bebe42b6001616”,
   “status”: “VOUCHING”, “vanity_id”: 1, “display_name”: “satoshin”,
   “first_name”: “Satoshi”, “last_name”: “Nakamoto”, “registered”: true,
   “photo”:
   “https://ipfs.kleros.io/ipfs/QmXmLgii8brfAP7edaabbRHey5VKvFhqqpSFfJf4sD1Lf6/image.jpg”,
   “video”:
   “https://ipfs.kleros.io/ipfs/QmXmLgii8brfAP7edaabbRHey5VKvFhqqpSFfJf4sD1Lf6/video.mp4”,
   “bio”: “Chancellor on brink of second bailout for banks.”, “profile”:
   “https://app.proofofhumanity.id/profile/0xf49a19f72d0e106df462cfd6b5bebe42b6001615”,
   “registered_time”: “2022-01-11T01:11:25.486Z”, “creation_time”:
   “2022-01-11T01:11:25.486Z” }

Independent Methods
-------------------

-  get_raw_list_of_humans: It returns a list of dicts with each human
   information based on the number and the “order_by” configuration you
   want.
-  get_raw_set_of_addresses: Similar to the previous ones but it returns
   a python set instead of a list. It is a bit faster.
-  get_list_of_humans: Similar to the previous ones, but this one
   returns a list of already instantiated Humans instead.
-  ping: Returns True if there is a correct conection to the Rest API.
-  is_registered: Returns True if the given ETH address is registered at
   Proof of Humanity.

Example of usage:

.. code:: python:

   list_of_humans = pypoh.get_list_of_humans(amount=10, order_by= "registered_time", order_direction = "desc", include_unregistered = False)

Acknowledgements
================

This python Wrapper uses this Rest API: https://api-kovan.poh.dev

License
=======

MIT License Copyright (c) 2018 YOUR NAME Permission is hereby granted,
free of charge, to any person obtaining a copy of this software and
associated documentation files (the “Software”), to deal in the Software
without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions: The above copyright
notice and this permission notice shall be included in all copies or
substantial portions of the Software. THE SOFTWARE IS PROVIDED “AS IS”,
WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

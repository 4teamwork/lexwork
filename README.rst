Lexwork API Client
==================

Mini API client to use the Lexwork PDF Signer developed by `Sitrox <https://www.sitrox.com>`.

Installation
------------

Installing it:

.. code-block:: bash

   pip install git+git://github.com/4teamwork/lexwork.git#egg=lexwork


Usage
-----

.. code-block:: python

   from lexwork.apiclient import APIClient

   client = APIClient(url='https://lexwork.example.org', username='user', password='secret')
   client.test() # Raises an exception if the request wasn't successful
   client.pdf_signature_reasons() # Returns an array of valid signature reasons

   # Returns the signed PDF as a base64 string
   signed_pdf = client.sign_pdf(file=file_like, reason_for_signature='something important')
   

   

Authentication
==============

The AHJ Registry API uses token-based authentication.
Follow the steps in **Creating an Account** and **Getting an API Token** to get an API token.
Look at the **API** section to learn what functionality is available and how to use the AHJ Registry API.

Creating an Account
-------------------

To create an account with the AHJ Registry, follow these steps:
    #. Visit the :ahjregistry:`AHJ Registry <>`, and click **Register** in the top-right corner.
    #. Fill out the sign up form, and click **Sign up**.
    #. Check your email to see a confirmation email sent from **ahjregistry@sunspec.org**. Open it and **click the link** to activate your account.
    #. After clicking the link, you will be directed to the login page. Another email will be sent to confirm your account was successfully activated.

Finding your API Token
----------------------

Find your API token by following these steps:
    #. Go to :AHJRegistry:, and click **Login** in the top-right corner. Login into your account.
    #. Go to your profile by clicking the arrow next to your account's profile picture in the top-right corner, and clicking **Profile** on the dropdown.
    #. On your profile page, click **Edit Profile**.
    #. Click the far-right tab labeled **API**.
    #. Here you will find your API token, whether it is activated, and when its activation will expire.

Activating your API Token
-------------------------

Your API token needs to be activated before you can use it. Please contact `membership@sunspec.org`_ to activate it.


Using your API Token
--------------------

An API token is required on every request to AHJ Registry API endpoints.
The API token should be included in the header of the HTTP request as follows:

.. code-block:: yaml

    Authorization: Token <api_token>

    # Example
    Authorization: Token 1dca175cd4d363ef6cb5e0a5425844a9f6cd247a3

.. Links

.. _membership@sunspec.org: mailto:membership@sunspec.org

Welcome To Open Falcon Portal
=========================

Hi! Nice to see you here!

If you'd like to ask a question
===============================

Please see [this web page ](http://book.open-falcon.com/) for community information, which includes falcon's wiki/FAQ and [IRC contacts](http://book.open-falcon.com/zh/authors.html).  

The github issue tracker is not the best place for questions for various reasons, but IRC is very helpful places for those things.

If you'd like to contribute code
================================

The project takes contributions through [github pull requests](https://help.github.com/articles/using-pull-requests)

It is usually a good idea to [join the QQ group](http://jq.qq.com/?_wv=1027&k=g8tvOZ) to discuss any large features prior to submission, and this especially helps in avoiding duplicate work or efforts where we decide, upon seeing a pull request for the first time, that revisions are needed. (This is not usually needed for frentend development, but can be nice for large changes).

If you'd like to file a bug
===========================

I'd also read the community page above, but in particular, make sure you copy [this issue template](https://github.com/open-falcon/portal/blob/master/ISSUE_TEMPLATE.md) into your ticket description. This template helps us organize tickets faster and prevents asking some repeated questions, so it's very helpful to us and we appreciate your help with it.

Also please make sure you are testing on the latest released version of Falcon modules or the development branch.

Thanks!

If you'd like to contribute translations
========================================

Portal project is based on Flask framework, we use the Flask-Babel extension to enable muti-language display support.

If you would like to help with the translation(i18n) works, whether correcting a typo or improving a section, or maybe even add a new language support, follow instractions bellow and submit a github pull request, it would be nice of you to read [this guide](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-i18n-and-l10n) before action.

    $ # activate python
    $ source env/bin/activate

    $ # run like this to add a new language translation file , otherwise skip this step
    $ python scripts/tr_init.py en_GB

    $ # update translation file
    $ python scripts/tr_uptate.py

    $ # translate all msgids, and ensure there is no fuzzy line left.
    $ vi web/translations/es/LC_MESSAGES/messages.po

    $ # update LANGUAGES in frame.config
    $ vi frame/config.py

    # # compile to use
    $ python scripts/tr_compile.py

    $ # have a test~
    $ python wsgi.py

    $ # create a pull request


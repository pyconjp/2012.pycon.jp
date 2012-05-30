================
 サイトについて
================

ビルド方法
==========

サイトのビルド時に Sphinx 拡張である sphinxcontrib.feed を使っています。
しかし、こいつは PyPI に上がっていないので sphinx/externals/feed にソースをまるっと突っ込んでいます。

buildout を使う
---------------

buildout を使うと何も考えずにビルドできるので楽です。

::

   $ # リポジトリのルートにいるとして
   $ cd sphinx
   $ buildout
   $ bin/make-docs


自力でがんばる
--------------

buildout しなくても sphinx/externals/feed を PYTHONPATH に追加するだけなのでそれほど面倒ではありません。
その場合でも sphinx は既にインストールされている必要があります。
また、 sphinx のバージョンが古いとエラーになるかもしれません。

::

   $ # リポジトリのルートにいるとして
   $ cd sphinx
   $ export PYTHONPATH=`pwd`/externals/feed
   $ make html




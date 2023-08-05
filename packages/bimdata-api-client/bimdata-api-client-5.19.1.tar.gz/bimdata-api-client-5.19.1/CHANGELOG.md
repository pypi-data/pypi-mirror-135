# Changelog

<!--next-version-placeholder-->

## v5.19.1 (2022-01-18)
### Fix
* Add non automatic models (#464)

* Add non automatic models

* improve tests

* rename route and add permissions

* add model delete with doc ([`b224801`](https://github.com/bimdata/python-api-client/commit/b2248010f7890245d90e9b4f067e4ca96ea00a63))

## v5.19.0 (2022-01-14)
### Feature
* Feature/smart files (#463)

* allow many model types

* add tests

* fix document name

* more cleanup

* update ci poetry version

* do not reprocess on file update

* fix export,merge and optimize queues

* add types.py

* more contants ([`a5ba918`](https://github.com/bimdata/python-api-client/commit/a5ba9187333e0a1b754b49755322102085adacc3))

## v5.18.3 (2022-01-11)
### Fix
* (visa) add validations_in_error to serializer ([`e4df33f`](https://github.com/bimdata/python-api-client/commit/e4df33ffcaf01b3f60f7e214a2a64809d2befcf3))

## v5.18.2 (2022-01-04)
### Fix
* Fix document elements list uuids ([`39de959`](https://github.com/bimdata/python-api-client/commit/39de959c2a58e9ab3b5949542efe76456cd8cad9))

## v5.18.1 (2021-12-22)
### Fix
* Rename element_ids to element_uuids ([`461e3db`](https://github.com/bimdata/python-api-client/commit/461e3db667d2edba71b1596d694185f61d3233b5))

## v5.18.0 (2021-12-22)
### Feature
* Add element/documents route ([`68a02e7`](https://github.com/bimdata/python-api-client/commit/68a02e7d227d78ef2e4efd9bdfbe82b1b686cf89))

## v5.17.1 (2021-12-13)
### Fix
* Add document to visa serializer ([#458](https://github.com/bimdata/python-api-client/issues/458)) ([`7504aee`](https://github.com/bimdata/python-api-client/commit/7504aee678ed033bcbe517ab9fcfe7c54776bfcf))

## v5.17.0 (2021-12-09)
### Feature
* Feature/link element document (#457)

* add documents to elements

* add test for filterred ifc and document list

* typo

* add some query optimizations ([`92814d1`](https://github.com/bimdata/python-api-client/commit/92814d193cd97e2feddbed979806ed702db7301d))

## v5.16.0 (2021-12-06)
### Feature
* Feature/visa (#451)

* add invitation to userProject

* PR changes requests

* init visa

* fix: boolean swagger bad import

* fix: git conflict migrations, replace tests 'put'

* add visa project view and change perform_created method on others views

* fix: duplicate swagger operation id on getComment*

* review PR and add permission mixin actions

* fix tests

* fix swagger

* add nested mixin to self visa project view

* fix creator filter view

* print test

* bypass schrodinger swagger pb

* clean useless db requests in permissions

* restore 404 ifc tests

* add userproject to serializers context ([`a963e5f`](https://github.com/bimdata/python-api-client/commit/a963e5f94af8f3e4d098856adc9253a0cb473252))

## v5.15.2 (2021-12-02)
### Fix
* Add id to Public Organization Serializer ([`5ac3574`](https://github.com/bimdata/python-api-client/commit/5ac357430084e206b40537112334d8de4075f805))

## v5.15.1 (2021-12-02)
### Fix
* Add organization serializer in App and MPApp serializers (#452)

* add organization serializer in App and MPApp serializers

* fix test and add select related

* use Public Organization Serializer ([`b1f0958`](https://github.com/bimdata/python-api-client/commit/b1f0958e511655ca19ddbf52ab35fbb1d1fd1fc2))

## v5.15.0 (2021-11-24)
### Feature
* Remove deprecated and put (#450)

* remove deprecated route and PUT route without BCF routes

* fix some tests

* fix last tests and restore project tree route

* restore BCF tests change

* rename fullUpdate operation ([`5769df5`](https://github.com/bimdata/python-api-client/commit/5769df5195f22e65696b4c46ed1a8ee925634526))
* Add leave project route (#449)

* Add leave project route

* fix roles ([`4d52c51`](https://github.com/bimdata/python-api-client/commit/4d52c51628bf3e977074dfec3d8af51615a13c2d))

### Fix
* Fix semantic release ([`aca3560`](https://github.com/bimdata/python-api-client/commit/aca3560c5d69a91d32be6992c0d8aea1153110b4))
* Fix serializer user project (#448)

Breaking Change:
 -  key to  for GroupUser create view
 - Route pk for userProject views is now UserProject pk and not FosUser pk

Some other change:
- fix serializer of userProject for swagger and libs
- add missing invitation user project from project and group
- fix some test ([`8b5446a`](https://github.com/bimdata/python-api-client/commit/8b5446a58252f767665f6cd3fff59af93baddfbd))
* Add invitation key in UserProject ([`30a8fb5`](https://github.com/bimdata/python-api-client/commit/30a8fb5ad88a6aed47de4bcb69a34cd37702e5ff))
* Get cloud size operation id in openapi ([`d508862`](https://github.com/bimdata/python-api-client/commit/d5088627492eec9d1ea02a8915cfb1d7ed4ce09c))
* Fix list/create methods openAPI ([`7519d93`](https://github.com/bimdata/python-api-client/commit/7519d931205caffc57f964e92e0547714d916304))

## v5.14.0 (2021-09-13)
### Feature
* Serialize user-permissions on documents ([`8597421`](https://github.com/bimdata/python-api-client/commit/859742176f6e0827c170dd8d30c95c254d502fcc))
* Add profile_picture field in user serialization

* add user picture field

* fix user.company, add comment about an edge case ([`45bd37c`](https://github.com/bimdata/python-api-client/commit/45bd37ce3e9ead5bb4050fa2a26a609a64e8ac26))
* Add GED permissions ([`00b987a`](https://github.com/bimdata/python-api-client/commit/00b987af3d7f310c07beb9d30c7354b9e5830d26))
* Allow bigger guids ([#420](https://github.com/bimdata/python-api-client/issues/420)) ([`54b2b09`](https://github.com/bimdata/python-api-client/commit/54b2b090cbbf127cf8ac0f17c3492e6d0e1c7f29))

### Fix
* Allow empty name in raw layers and raw materials ([`b96d9a7`](https://github.com/bimdata/python-api-client/commit/b96d9a7eb1e3828fd2b3f7e9edb558b296d38f0b))
* Allow empty name in raw layers and raw materials ([`c0d6bb6`](https://github.com/bimdata/python-api-client/commit/c0d6bb6f662d3289915da48580553bb2277c7ee7))
* Allow empty name in raw layers and raw materials ([`22e450d`](https://github.com/bimdata/python-api-client/commit/22e450d38322621610ca85750524c94dd197f33c))
* Fix dms-tree group permissions ([`38f8ce5`](https://github.com/bimdata/python-api-client/commit/38f8ce5608ad11f8dd1518a9a901da5ef8779bdd))
* Fix field name and add field to children dms-tree ([#426](https://github.com/bimdata/python-api-client/issues/426)) ([`2881af8`](https://github.com/bimdata/python-api-client/commit/2881af81fb7ae5fe2718f8187ffc5ae350aa4ebd))

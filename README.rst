***************************
interlegis.portalmodelo.api
***************************

.. contents:: Conteúdo
   :depth: 2

Introdução
==========

Este pacote fornece um configlet do painel de controle do Plone para cadastar
os dados básicos da Casa Legislativa:

* Nome do órgão
* Tipo do órgão
* Endereço
* CEP
* Cidade
* Estado
* CNPJ
* Telefone
* Email

O pacote também fornece duas views para consulta de informação em formato
JSON.

Detalhes da implementação
=========================

Nome do órgão
-------------

O campo nome do órgão deve ficar sempre sincronizado com o título do portal.

A implementação é simples: no render do formulario o valor do campo é
atualizado com o valor da propriedade ``title`` do portal::

    def updateWidgets(self):
        ...
        portal = api.portal.get()
        self.widgets['title'].value = portal.title

Na hora de guardar o formulario, usamos um ``invariant`` como hook para
colocar essa misma informação de volta::

    @invariant
    def update_portal_title_hook(data):
        portal = api.portal.get()
        portal.title = data.title

Desse jeito não importa se o usuário modifica o nome do órgão num formulario
ou no outro.

Tipo do órgão
-------------

O tipo de órgão é um vocabulário controlado com os seguinte valores possíveis:

* Assembleia Legislativa
* Câmara dos Deputados
* Câmara Legislativa
* Câmara Municipal
* Outro
* Senado Federal
* Tribunal de Contas da União
* Tribunal de Contas Estadual
* Tribunal de Contas Municipal

JSON API
--------

O pacote fornece duas views na raiz do portal para consulta de informação em
formato JSON: ``@@portalmodelo-json`` e ``@@transparency-json``.

``@@portalmodelo-json``
^^^^^^^^^^^^^^^^^^^^^^^

Disponibiliza a informação básica da Casa Legislativa que foi cadastrada no
configlet do painel de controle do portal::

    {
        "address": "Rua Comendador Roberto Ugolini, 20",
        "city": "Mooca",
        "email": "foo@bar.com",
        "id": "62.863.444/0001-08",
        "kind": "assembleia-legislativa",
        "postal_code": "03125-010",
        "state": "SP",
        "telephone": "+55 11 2271-2000",
        "title": "Portal Modelo"
    }

``@@transparency-json``
^^^^^^^^^^^^^^^^^^^^^^^^

Disponibiliza o conteúdo publicado dentro da estrutura de pastas definida para
cumprir com a Lei de Transparência::

    {
        "acompanhamento": [],
        "despesas": [
            {
                "creation_date": "2014-04-23T22:21:53-03:00",
                "description": "Arquivo em formato CSV.",
                "modification_date": "2014-04-23T22:21:53-03:00",
                "title": "Despesas de 201401",
                "uri": "http://localhost:8080/portal/transparencia/despesas/despesas-de-201401"
            }
        ],
        "licitacoes": [],
        "receitas": [],
        "transferencias": []
    }

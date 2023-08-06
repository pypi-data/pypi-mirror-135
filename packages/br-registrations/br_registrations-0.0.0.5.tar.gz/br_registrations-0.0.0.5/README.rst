.. _BR-registrations:

BR registrations
================
|build-status|

.. |build-status| image:: https://img.shields.io/github/license/sliatecinos/br_registrations?style=plastic
    :alt: GitHub license   
    :target: https://github.com/sliatecinos/br_registrations/blob/master/LICENSE.txt


**Project description**
-----------------------
.. begin-docs

A simple Python library containing functions that check Brazilian documents values. It is intended to make it easy to verify CNPJ and CPF numbers.
Originally developed and open-sourced at `Sliatecinos (GitHub) <https://github.com/sliatecinos>`_.


**Installation**
----------------
.. begin-installation

``pip install br-registrations``

.. end-installation

**Basic Usage**
---------------
.. begin-usage

.. code:: python

    from br_registrations import validateCNPJ, validateCPF

    # Validation test of registration CNPJ number
    # Instances the validation:
    cnpj=validateCNPJ.CNPJ
    # Passing a 14-digit number of CNPJ (in string format):
    response=cnpj.valid_cnpj('11222333000181')
    # Output: 'CNPJ is valid is True .'
    print('CNPJ is valid is', response, '.')

    # Passing a registration number of CNPJ (in string format):
    dv=cnpj.get_cnpj_dv('112223330001')
    print('Correct DV: ', dv)
    # Output (in list): 'Correct DV:  [8, 1]'

    print('='*100)

    # Validation test of registration CPF number
    # Instances the validation
    cpf=validateCPF.CPF
    # Passing a 11-digit number of CPF (in string format):
    response=cpf.valid_cpf('11144477735')
    # Output: 'CPF is valid is True .'
    print('CPF is valid is', response, '.')

    # Passing a registration number of CPF (in string format):
    dv=cpf.get_cpf_dv('111444777')
    print('Correct DV: ', dv)
    # Output (in list): 'Correct DV:  [3, 5]'

    # View lib version:
    import br_registrations as brr
    print(brr.__version__)

.. end-usage

Links
-----
* PyPi.org: `https://pypi.org/project/br-registrations <https://pypi.org/project/br-registrations/>`_

* Source code: `https://github.com/sliatecinos/br-registrations <BR-registrations_>`__

License
-------

The project is made available under the terms of the MIT license.  See `LICENSE <./LICENSE>`_ for details.

.. end-docs

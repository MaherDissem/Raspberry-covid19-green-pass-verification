# Raspberry covid19 green pass verification

<p align="center" width="100%">
    <img src="./img/hardware-setup.jpg" alt="drawing" style="float: right;" width="200"/>
    <img src="./img/use-case.jpg" alt="drawing" style="float: right;" width="200"/>

</p>


A camera client written in Python detects, decodes and decrypt QR codes and sends them to the validation server, written in Node.js.

The validation server does formal verification including
verifying the signature and the business rules.

Result (pass informations / 'invalid') is displayed on the screen.

<img align="center" src="./img/architecture.png" alt="drawing" width="600"/>

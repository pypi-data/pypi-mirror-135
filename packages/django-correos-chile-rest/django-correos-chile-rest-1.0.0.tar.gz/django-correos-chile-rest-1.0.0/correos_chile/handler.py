# -*- coding: utf-8 -*-
import logging
from django.template.loader import render_to_string
from django.http import HttpResponse
from correos_chile.connector import Connector, ConnectorException
from correos_chile.settings import api_settings

logger = logging.getLogger(__name__)


class CorreosHandler:
    """
        Handler to send shipping payload to Correos
    """

    def __init__(self, base_url=api_settings.CORREOS_CHILE['BASE_URL'],
                 token=api_settings.CORREOS_CHILE['TOKEN'],
                 verify=True):
        self.base_url = base_url
        self.token = token
        self.verify = verify
        self.connector = Connector(self._headers(), verify_ssl=self.verify)

    def _headers(self):
        """
            Here define the headers for all connections with Correos.
        """
        return {
            'Authorization': f'token {self.token}',
            'Content-Type': 'application/json',
        }

    def get_shipping_label(self, instance, response_data):
        raise NotImplementedError(
            'get_shipping_label is not a method implemented for CorreosHandler')

    def get_default_payload(self, instance):
        """
            This method generates by default all the necessary data with
            an appropriate structure for Rayo courier.
        """
        payload = {
            "nroDTE": 0,
            "codCliente": api_settings.SENDER['CLIENT'],
            "posicionInicial": 0,
            "formatoEtiqueta": "PDF",
            "modo": "json",
            "data": [
                {
                    "codAdmision": api_settings.SENDER['ADMISSION'],
                    "codCentro": "",
                    "codServicio": api_settings.CORREOS_CHILE['COD_SERVICIO'],
                    "remitente": {
                        "nombre": api_settings.SENDER['NAME'],
                        "codPais": api_settings.SENDER['COUNTRY'],
                        "comuna": api_settings.SENDER['CITY'],
                        "direccion": api_settings.SENDER['ADDRESS'],
                        "codPostal": "",
                        "rut": api_settings.SENDER['RUT'],
                        "contacto": api_settings.SENDER['CONTACT_NAME'],
                        "telefono": api_settings.SENDER['CONTACT_PHONE'],
                        "email": ""
                    },
                    "destinatario": {
                        "nombre": instance.customer.full_name,
                        "codPais": api_settings.SENDER['COUNTRY'],
                        "comuna": instance.commune.name,
                        "direccion": f'{instance.address.street} {instance.address.number}',
                        "codPostal": instance.commune.code,
                        "rut": instance.customer.rut,
                        "contacto": instance.customer.full_name,
                        "telefono": instance.customer.phone,
                        "email": ""
                    },
                    "pagoSeguro": '',
                    "bultos": 1,
                    "kilos": 1,
                    "volumen": 0,
                    "codReferencia": f"{api_settings.CORREOS_CHILE['COD_REF']} - {instance.reference}",
                    "observaciones": "",
                    "observacionesInternas": "",
                    "tipoMercancia": "",
                    "tipoPortes": api_settings.CORREOS_CHILE['TYPE_POR'],
                    "valorDeclarado": 0,
                    "devolucionConforme": api_settings.CORREOS_CHILE['DEV_CON'],
                    "importeReembolso": 0,
                    "numDocumentos": 0
                }
            ]
        }
        logger.debug(payload)
        return payload

    def create_shipping(self, data):
        """
            This method generate a Correos chile admision.
            If the get_default_payload method returns data, send it here,
            otherwise, generate your own payload.
        """

        url = f'{self.base_url}etiquetas'
        logger.debug(data)
        try:
            response = self.connector.post(url, data)
            response.update({'tracking_number': response['info'][0]['admision']['numeroEnvio']})
            response.update({'base64': response['archivos'][0]['str64Data']})
            return response

        except ConnectorException as error:
            logger.error(error)
            raise ConnectorException(error.message, error.description, error.code) from error

    def get_tracking(self, identifier):
        raise NotImplementedError(
            'get_tracking is not a method implemented for CorreosHandler')

    def get_events(self, raw_data):
        raise NotImplementedError(
            'get_events is not a method implemented for CorreosHandler')

    def get_status(self, raw_data):
        raise NotImplementedError(
            'get_status is not a method implemented for CorreosHandler')
# -*- coding: utf-8 -*-
from pd.prenotazioni.browser.prenotazione_print import PrenotazionePrint
from pd.prenotazioni.browser.prenotazione_print_pdf import PrenotazionePrintPDF


class CCPDPrenotazionePrint(PrenotazionePrint):
    """
    This is a view to proxy autorizzazione
    """

    description = u"La conferma sarà inviata alla mail"


class CCPDPrenotazionePrintPDF(PrenotazionePrintPDF):
    """
    This is a view to proxy autorizzazione
    """

    footer_text = "Camera di commercio di Padova"

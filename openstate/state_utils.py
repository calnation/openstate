def chamber_name(bill_chamber, state='CA'):
    if state == 'CA':
        if bill_chamber == 'upper':
            return 'Senate'
        elif bill_chamber == 'lower':
            return 'Assembly'
        else:
            return 'Joint'
    else:
        return None


def term_name(term, state='CA'):
    """
    An internal method for converting API strings to readable ones, i.e. '20172018' => '2017-18'
    Args:
        term: term name as it comes from OpenStates API

    Returns:
        String transformed
    """
    if state == 'CA':
        return term[0:4] + '-' + term[6:]
    else:
        return None

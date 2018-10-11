from Tables import Tables


class BillSponsor(Tables):

    def __init__(self):
        Tables.__init__(self)
        self.template_name = 'Relation:BillSponsor'


def sponsorship_type(sponsor):
    sponsorship_type_dic = {
        'primary': 'Lead Author',
        'author': 'Lead Author',
        'principal coauthor': 'Principal Coauthor',
        'cosponsor': 'Coauthor',
        'coauthor': 'Coauthor',
    }
    if sponsor['official_type']:
        _type = sponsor['official_type'].replace("_", " ").lower()
    else:
        _type = sponsor['type'].lower()
    return sponsorship_type_dic[_type]


def table_rows(bill_dic):
    sponsorships = []
    if bill_dic['sponsors']:
        for sponsorship in bill_dic['sponsors']:
            new_sponsorship = {
                'os_bill_id': bill_dic['id'],
                'os_leg_id': sponsorship.get('leg_id'),
                'committee_id': sponsorship.get('committee_id'),
                'sponsorship_type': sponsorship_type(sponsorship['type']),
            }

            # TODO find id using name?
            if new_sponsorship['os_leg_id'] == new_sponsorship['committee_id'] is None:
                new_sponsorship.update({'name': sponsorship.get('name')})

            sponsorships.append(new_sponsorship)

    return sponsorships

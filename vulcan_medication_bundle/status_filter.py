# AUTOGENERATED! DO NOT EDIT! File to edit: 20a_status_filter.ipynb (unless otherwise specified).

__all__ = ['CM_EXCLUDE_STATUS_MAP', 'get_negated_list']

# Cell
from .core import *

# Cell
# Note: this is using med-status.xlsx values
CM_EXCLUDE_STATUS_MAP = dict(
        MedicationRequest=['cancelled','entered-in-error','stopped','draft'],
        MedicationDispense=['cancelled','entered-in-error','stopped','declined'],
        MedicationAdministration=['not-done','entered-in-error'],
        MedicationStatement=['entered-in-error','not-taken'])

# Cell
def _new_list_entry(reference, resourceType, status, statuses_to_remove):
    return {'item': {'reference': reference},
            'flag': {'text': f"{resourceType} negated as its status '{status}' is one of {statuses_to_remove}"}}

def get_negated_list(bundle, exclude_status_map=CM_EXCLUDE_STATUS_MAP):
    result = new_list('Negated list of medications')
    # put the status map in an annotation
    result['note'] = [dict(text=f'Exclude status map: ```{exclude_status_map}```')]
    for entry in bundle.get('entry', []):
        resource = entry.get('resource', {})
        resourceType, status = resource.get('resourceType'), resource.get('status')
        statuses_to_remove = exclude_status_map.get(resourceType)
        if statuses_to_remove is not None and status in statuses_to_remove:
            result['entry'].append(_new_list_entry(
                entry['fullUrl'], resourceType, status, statuses_to_remove))
    if not result['entry']: del result['entry']
    return result
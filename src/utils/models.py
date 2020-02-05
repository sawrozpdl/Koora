from django.db.models import Model, QuerySet
from django.forms.models import model_to_dict


def nested_model_to_dict(model):

    if hasattr(model, 'to_dict'):
        dict_obj = model.to_dict()

    elif isinstance(model, list):
        return list(map(lambda item : nested_model_to_dict(item), model))
    
    elif isinstance(model, QuerySet):
        return nested_model_to_dict(list(model))

    elif isinstance(model, Model):
        # have to use model_to_dict for fact that some fields go missing with __dict__ with unnessary fields addition
        dict_obj = model_to_dict(model)
    
    elif hasattr(model, '__dict__'):
        dict_obj = model.__dict__
    
    else:
        return model
    
    for key in dict_obj:
        dict_obj[key] = nested_model_to_dict(dict_obj[key])
    
    return dict_obj

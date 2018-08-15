from rest_framework import routers, serializers as ser
from dynamicforms.viewsets import ModelViewSet
from dynamicforms import serializers
from .models import Validated


# TODO: templates/examples/base* je treba prenest v dynamicforms/templates
# TODO: Vnos recordov narediti preko dialoga
# TODO:   zadeva mora biti nastavljiva: tako kot sedaj ali pa dialog
# TODO:   oziroma: programer sam se odloči točno kaj se zgodi, ko se klikne "add" ali "edit" - tudi nekaj povsem tretjega...
# TODO: AJAX za vnos recordov?
# TODO: paginate list template (ne zriši vseh 1500 recordov takoj, ampak jih dinamično loadaj, ko user poscrolla dovolj daleč dol
# TODO:   pagination lahko narediš na dva načina:
# TODO:     1. lahko imaš nek element pod tabelo in ko ta element pade v view, poskušaš naložit dodatne recorde
# TODO:     2. lahko pa enemu od recordov proti koncu tabele obesiš to funkcionalnost in bo začel nalagat, ko ON pride v view. tako imaš možnost, da bi bili novi podatki naloženi še preden jih user dejansko potrebuje


class ValidatedSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)  # so that it shows at all

    class Meta:
        model = Validated
        exclude = ()


class ValidatedViewSet(ModelViewSet):
    # renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'examples/validated.html'
    list_template_name = 'examples/validated_list.html'
    template_context = dict(crud_form=True)

    queryset = Validated.objects.all()
    serializer_class = ValidatedSerializer


router = routers.DefaultRouter()
router.register(r'rest/validated', ValidatedViewSet, base_name='validated')

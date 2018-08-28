from rest_framework import routers
from rest_framework.exceptions import ValidationError
from dynamicforms.viewsets import ModelViewSet
from dynamicforms import serializers
from .models import Validated


# TODO: templates/examples/validated* je treba prenest v dynamicforms/templates (standardni templati morajo bit pokrit)
# TODO: Vnos recordov narediti preko dialoga
# TODO:   zadeva mora biti nastavljiva: tako kot sedaj ali pa dialog
# TODO:   oziroma: programer sam se odloči točno kaj se zgodi, ko se klikne "add" ali "edit" - tudi nekaj povsem tretjega...
# TODO: paginate list template (ne zriši vseh 1500 recordov takoj, ampak jih dinamično loadaj, ko user poscrolla dovolj daleč dol
# TODO:   pagination lahko narediš na dva načina:
# TODO:     1. lahko imaš nek element pod tabelo in ko ta element pade v view, poskušaš naložit dodatne recorde
# TODO:     2. lahko pa enemu od recordov proti koncu tabele obesiš to funkcionalnost in bo začel nalagat, ko ON pride v view. tako imaš možnost, da bi bili novi podatki naloženi še preden jih user dejansko potrebuje


class ValidatedSerializer(serializers.ModelSerializer):

    form_titles = {
        'table': 'Validated list',
        'new': 'New validated object',
        'edit': 'Editing validated object',
    }
    # id = serializers.IntegerField(required=False)  # so that it shows at all

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['amount'] != 5:
            if attrs['code'] != '123':
                raise ValidationError({'amount': 'amount can only be different than 5 if code is "123"'})
        # dodaj še enega brez veznega za celo formo, samo tolk, da se bo videlo, da se zriše zgoraj
        return attrs

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

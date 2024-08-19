import time

from django.http.response import HttpResponse
from rest_framework.renderers import JSONRenderer

from dynamicforms import fields, serializers, viewsets
from dynamicforms.action import Actions, FormButtonAction, FormButtonTypes
from dynamicforms.mixins import DisplayMode
from dynamicforms.progress import get_progress_key, set_progress_comment, set_progress_value
from dynamicforms.template_render.layout import Group, Layout, Row


class AddressSerializer(serializers.Serializer):
    street = fields.CharField(max_length=100)
    city = fields.CharField(max_length=50)
    country = fields.CharField(max_length=50)


class SingleDialogSerializer(serializers.Serializer):
    template_context = dict(url_reverse="single-dialog", size="large")
    form_titles = {
        "table": "",
        "new": "Create a travel plan",
        "edit": "",
    }
    show_filter = False

    actions = Actions(
        FormButtonAction(FormButtonTypes.CANCEL, name="cancel"),
        FormButtonAction(FormButtonTypes.CUSTOM, name="download", label="Download it"),
        FormButtonAction(FormButtonTypes.CUSTOM, name="say_it", label="Say it", button_is_primary=True),
        add_form_buttons=False,
    )

    download = fields.IntegerField(max_value=1, default=0, display_form=DisplayMode.HIDDEN)
    name = fields.CharField(max_length=100, label="Your Name")
    email = fields.EmailField(label="Email Address")
    travel_type = fields.ChoiceField(
        label="Type of Travel",
        choices=(("Business", "Business"), ("Leisure", "Leisure"), ("Adventure", "Adventure")),
    )
    destination = fields.CharField(max_length=100, label="Destination")
    start_date = fields.DateField(label="Start Date")
    end_date = fields.DateField(label="End Date")
    address = AddressSerializer(label="Contact Address")

    class Meta:
        layout = Layout(
            Row('name', 'email'),
            Row('travel_type'),
            Row(Group(
                None, title="Trip Details", sub_layout=Layout(
                    Row('destination'),
                    Row('start_date', 'end_date'),
                    auto_add_fields=False,
                )
            )),
            Row(Group('address', title="Contact Address")),
        )


class SingleDialogViewSet(viewsets.SingleRecordViewSet):
    serializer_class = SingleDialogSerializer

    def new_object(self):
        return dict(
            name=None,
            email=None,
            travel_type=None,
            destination=None,
            start_date=None,
            end_date=None,
            address=dict(street=None, city=None, country=None)
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        if str(request.data.get("download", "")) == "1":
            itinerary = f"Travel Itinerary for {data['name']}\n\n"
            itinerary += f"Destination: {data['destination']}\n"
            itinerary += f"Travel Type: {data['travel_type']}\n"
            itinerary += f"Date: {data['start_date']} to {data['end_date']}\n"
            res = HttpResponse(itinerary.encode("utf-8"), content_type="text/plain; charset=UTF-8")
            res["Content-Disposition"] = "attachment; filename={}".format("travel_itinerary.txt")
            return res

        progress_key = get_progress_key(request)
        for i in range(10):
            set_progress_comment(progress_key, "Processing #%d" % (i + 1))
            set_progress_value(progress_key, (i + 1) * 10)
            time.sleep(0.5)

        return HttpResponse(JSONRenderer().render(data), content_type="application/json")

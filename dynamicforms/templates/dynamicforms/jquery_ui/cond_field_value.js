function cond() {
  {% if matching_values_is_list %}
    var vals = ({{ matching_values }});
    return vals.indexOf({{ field_value }}) > -1;
  {% else %}
    return ({{ matching_values }}) == {{ field_value }};
  {% endif %}
}

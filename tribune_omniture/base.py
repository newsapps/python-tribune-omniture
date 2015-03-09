from .utils import to_camelcase

def generate_data_object_script(**kwargs):
    """Generate JavaScript to configure third party analytics service"""
    bits = []

    bits.append("<script>")

    bits.append("((((window.trb || (window.trb = {})).data || "
        "(trb.data = {})).metrics || (trb.data.metrics = {})).thirdparty = {")

    for key, value in kwargs.items():
        js_key = to_camelcase(key)
        bits.append("  {key}: '{value}',".format(key=js_key, value=value))

    bits[-1] = bits[-1].rstrip(',')

    bits.append("});")

    bits.append("</script>")


    return "\n".join(bits)

def generate_thirdpartyservice_script(domain, disable_nav=True, disable_ssor=True):
    qs_bits = []

    if disable_nav is True:
        qs_bits.append("disablenav=true")

    if disable_ssor is True:
        qs_bits.append("disablessor=true")

    qs = "&".join(qs_bits)

    url = "//" + domain + "/thirdpartyservice"

    if qs:
        url = url + "?" + qs

    script = "<script src='" + url + "' async></script>"

    return script

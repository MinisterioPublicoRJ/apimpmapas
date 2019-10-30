from django.utils.text import capfirst

entidade_name = 'entidade'
dado_1_id = 0
dado_1_title = 'dado_1'
dado_2_id = 1
dado_2_title = 'dado_2'
dado_base_1_id = 2
dado_base_1_title = 'base_1'
dado_base_2_id = 3
dado_base_2_title = 'base_2'

hidden_field = 'input type="hidden" name="action" value="change_to_detail"'
html_list = (
                f'Você deseja colocar as caixinhas seleciondas: <br>\n'
                f'<ul>\n  \n    '
                f'<li>{dado_1_title}</li>\n  \n    '
                f'<li>{dado_2_title}</li>\n  \n'
                f'</ul>\n'
                f'Da entidade {entidade_name} como detalhe de qual caixinha?'
            )
id_fields = (
                f'<input type="hidden" name="_selected_action"'
                f' value="{dado_1_id}" />\n    \n      '
                f'<input type="hidden" name="_selected_action"'
                f' value="{dado_2_id}" />'
            )
form_select = (
                f'<select id="dado_base" name="dado_base">\n    \n      '
                f'<option value="{dado_base_1_id}" >\n        '
                f'{capfirst(dado_base_1_title)}\n      '
                f'</option>\n    \n      '
                f'<option value="{dado_base_2_id}" >\n        '
                f'{capfirst(dado_base_2_title)}\n      '
                f'</option>\n    \n    '
                f'</select>'
            )
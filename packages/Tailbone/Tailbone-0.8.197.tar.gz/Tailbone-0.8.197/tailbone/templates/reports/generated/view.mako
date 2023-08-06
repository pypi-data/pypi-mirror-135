## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('{}.generate'.format(permission_prefix)):
      <li>${h.link_to("Generate new Report", url('generate_report'))}</li>
  % endif
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    % if params_data is not Undefined:
        ${form.component_studly}Data.paramsData = ${json.dumps(params_data)|n}
    % endif

  </script>
</%def>


${parent.body()}

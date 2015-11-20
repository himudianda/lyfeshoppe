from flask import Blueprint, render_template

sample_dashboard = Blueprint('sample_dashboard', __name__, template_folder='templates')


@sample_dashboard.route('/tmpFrameset')
def tmpFrameset():
    return render_template('sample_dashboard/tmpFrameset.html')


@sample_dashboard.route('/components_code_editors')
def components_code_editors():
    return render_template('sample_dashboard/components_code_editors.html')


@sample_dashboard.route('/agenda_views')
def agenda_views():
    return render_template('sample_dashboard/agenda-views.html')


@sample_dashboard.route('/stock_csv_data_and_events')
def stock_csv_data_and_events():
    return render_template('sample_dashboard/stock_csv_data_and_events.html')


@sample_dashboard.route('/ui_nestable')
def ui_nestable():
    return render_template('sample_dashboard/ui_nestable.html')


@sample_dashboard.route('/form_image_crop')
def form_image_crop():
    return render_template('sample_dashboard/form_image_crop.html')


@sample_dashboard.route('/multi')
def multi():
    return render_template('sample_dashboard/multi.html')


@sample_dashboard.route('/form_validation_states_md')
def form_validation_states_md():
    return render_template('sample_dashboard/form_validation_states_md.html')


@sample_dashboard.route('/portlet_ajax')
def portlet_ajax():
    return render_template('sample_dashboard/portlet_ajax.html')


@sample_dashboard.route('/specs')
def specs():
    return render_template('sample_dashboard/specs.html')


@sample_dashboard.route('/json')
def json():
    return render_template('sample_dashboard/json.html')


@sample_dashboard.route('/form_dropzone')
def form_dropzone():
    return render_template('sample_dashboard/form_dropzone.html')


@sample_dashboard.route('/form_wizard')
def form_wizard():
    return render_template('sample_dashboard/form_wizard.html')


@sample_dashboard.route('/uicolor')
def uicolor():
    return render_template('sample_dashboard/uicolor.html')


@sample_dashboard.route('/tabindex')
def tabindex():
    return render_template('sample_dashboard/tabindex.html')


@sample_dashboard.route('/page_user_profile_1')
def page_user_profile_1():
    return render_template('sample_dashboard/page_user_profile_1.html')


@sample_dashboard.route('/page_general_pricing')
def page_general_pricing():
    return render_template('sample_dashboard/page_general_pricing.html')


@sample_dashboard.route('/app_calendar')
def app_calendar():
    return render_template('sample_dashboard/app_calendar.html')


@sample_dashboard.route('/germany')
def germany():
    return render_template('sample_dashboard/germany.html')


@sample_dashboard.route('/days')
def days():
    return render_template('sample_dashboard/days.html')


@sample_dashboard.route('/donut_colors')
def donut_colors():
    return render_template('sample_dashboard/donut-colors.html')


@sample_dashboard.route('/timezones')
def timezones():
    return render_template('sample_dashboard/timezones.html')


@sample_dashboard.route('/bar')
def bar():
    return render_template('sample_dashboard/bar.html')


@sample_dashboard.route('/ui_idle_timeout')
def ui_idle_timeout():
    return render_template('sample_dashboard/ui_idle_timeout.html')


@sample_dashboard.route('/radar')
def radar():
    return render_template('sample_dashboard/radar.html')


@sample_dashboard.route('/app_inbox')
def app_inbox():
    return render_template('sample_dashboard/app_inbox.html')


@sample_dashboard.route('/form_input_mask')
def form_input_mask():
    return render_template('sample_dashboard/form_input_mask.html')


@sample_dashboard.route('/toolbar')
def toolbar():
    return render_template('sample_dashboard/toolbar.html')


@sample_dashboard.route('/portlet_draggable')
def portlet_draggable():
    return render_template('sample_dashboard/portlet_draggable.html')


@sample_dashboard.route('/fullpage')
def fullpage():
    return render_template('sample_dashboard/fullpage.html')


@sample_dashboard.route('/table_datatables_fixedheader')
def table_datatables_fixedheader():
    return render_template('sample_dashboard/table_datatables_fixedheader.html')


@sample_dashboard.route('/xhtmlstyle')
def xhtmlstyle():
    return render_template('sample_dashboard/xhtmlstyle.html')


@sample_dashboard.route('/form_fileupload')
def form_fileupload():
    return render_template('sample_dashboard/form_fileupload.html')


@sample_dashboard.route('/ui_session_timeout')
def ui_session_timeout():
    return render_template('sample_dashboard/ui_session_timeout.html')


@sample_dashboard.route('/table_datatables_rowreorder')
def table_datatables_rowreorder():
    return render_template('sample_dashboard/table_datatables_rowreorder.html')


@sample_dashboard.route('/ui_page_progress_style_1')
def ui_page_progress_style_1():
    return render_template('sample_dashboard/ui_page_progress_style_1.html')


@sample_dashboard.route('/page_general_search_3')
def page_general_search_3():
    return render_template('sample_dashboard/page_general_search_3.html')


@sample_dashboard.route('/inlinebycode')
def inlinebycode():
    return render_template('sample_dashboard/inlinebycode.html')


@sample_dashboard.route('/updating')
def updating():
    return render_template('sample_dashboard/updating.html')


@sample_dashboard.route('/portlet_ajax_content_2')
def portlet_ajax_content_2():
    return render_template('sample_dashboard/portlet_ajax_content_2.html')


@sample_dashboard.route('/form_controls_md')
def form_controls_md():
    return render_template('sample_dashboard/form_controls_md.html')


@sample_dashboard.route('/serial2')
def serial2():
    return render_template('sample_dashboard/serial2.html')


@sample_dashboard.route('/divreplace')
def divreplace():
    return render_template('sample_dashboard/divreplace.html')


@sample_dashboard.route('/default')
def default():
    return render_template('sample_dashboard/default.html')


@sample_dashboard.route('/map')
def map():
    return render_template('sample_dashboard/map.html')


@sample_dashboard.route('/appendto')
def appendto():
    return render_template('sample_dashboard/appendto.html')


@sample_dashboard.route('/layout_full_height_content')
def layout_full_height_content():
    return render_template('sample_dashboard/layout_full_height_content.html')


@sample_dashboard.route('/form_icheck')
def form_icheck():
    return render_template('sample_dashboard/form_icheck.html')


@sample_dashboard.route('/charts_highcharts')
def charts_highcharts():
    return render_template('sample_dashboard/charts_highcharts.html')


@sample_dashboard.route('/page_system_404_2')
def page_system_404_2():
    return render_template('sample_dashboard/page_system_404_2.html')


@sample_dashboard.route('/basic_views')
def basic_views():
    return render_template('sample_dashboard/basic-views.html')


@sample_dashboard.route('/ui_confirmations')
def ui_confirmations():
    return render_template('sample_dashboard/ui_confirmations.html')


@sample_dashboard.route('/table_datatables_buttons')
def table_datatables_buttons():
    return render_template('sample_dashboard/table_datatables_buttons.html')


@sample_dashboard.route('/stacked_bars')
def stacked_bars():
    return render_template('sample_dashboard/stacked_bars.html')


@sample_dashboard.route('/page_user_profile_1_help')
def page_user_profile_1_help():
    return render_template('sample_dashboard/page_user_profile_1_help.html')


@sample_dashboard.route('/serial_json')
def serial_json():
    return render_template('sample_dashboard/serial_json.html')


@sample_dashboard.route('/external_dragging')
def external_dragging():
    return render_template('sample_dashboard/external-dragging.html')


@sample_dashboard.route('/components_bootstrap_tagsinput')
def components_bootstrap_tagsinput():
    return render_template('sample_dashboard/components_bootstrap_tagsinput.html')


@sample_dashboard.route('/non_continuous')
def non_continuous():
    return render_template('sample_dashboard/non-continuous.html')


@sample_dashboard.route('/demo')
def demo():
    return render_template('sample_dashboard/demo.html')


@sample_dashboard.route('/loadMore2')
def loadMore2():
    return render_template('sample_dashboard/loadMore2.html')


@sample_dashboard.route('/inlineall')
def inlineall():
    return render_template('sample_dashboard/inlineall.html')


@sample_dashboard.route('/app_todo_2')
def app_todo_2():
    return render_template('sample_dashboard/app_todo_2.html')


@sample_dashboard.route('/ui_alerts_api')
def ui_alerts_api():
    return render_template('sample_dashboard/ui_alerts_api.html')


@sample_dashboard.route('/form_layouts')
def form_layouts():
    return render_template('sample_dashboard/form_layouts.html')


@sample_dashboard.route('/ui_modals')
def ui_modals():
    return render_template('sample_dashboard/ui_modals.html')


@sample_dashboard.route('/quarters')
def quarters():
    return render_template('sample_dashboard/quarters.html')


@sample_dashboard.route('/project3')
def project3():
    return render_template('sample_dashboard/project3.html')


@sample_dashboard.route('/readme')
def readme():
    return render_template('sample_dashboard/readme.html')


@sample_dashboard.route('/continents')
def continents():
    return render_template('sample_dashboard/continents.html')


@sample_dashboard.route('/serial_with_dynamic_graphs')
def serial_with_dynamic_graphs():
    return render_template('sample_dashboard/serial_with_dynamic_graphs.html')


@sample_dashboard.route('/bar_no_axes')
def bar_no_axes():
    return render_template('sample_dashboard/bar-no-axes.html')


@sample_dashboard.route('/app_inbox_inbox')
def app_inbox_inbox():
    return render_template('sample_dashboard/app_inbox_inbox.html')


@sample_dashboard.route('/ui_toastr')
def ui_toastr():
    return render_template('sample_dashboard/ui_toastr.html')


@sample_dashboard.route('/ui_blockui')
def ui_blockui():
    return render_template('sample_dashboard/ui_blockui.html')


@sample_dashboard.route('/ui_tiles')
def ui_tiles():
    return render_template('sample_dashboard/ui_tiles.html')


@sample_dashboard.route('/page_user_login_1')
def page_user_login_1():
    return render_template('sample_dashboard/page_user_login_1.html')


@sample_dashboard.route('/outputhtml')
def outputhtml():
    return render_template('sample_dashboard/outputhtml.html')


@sample_dashboard.route('/canada')
def canada():
    return render_template('sample_dashboard/canada.html')


@sample_dashboard.route('/page_general_contact')
def page_general_contact():
    return render_template('sample_dashboard/page_general_contact.html')


@sample_dashboard.route('/ciframe')
def ciframe():
    return render_template('sample_dashboard/ciframe.html')


@sample_dashboard.route('/pie_json')
def pie_json():
    return render_template('sample_dashboard/pie_json.html')


@sample_dashboard.route('/page_general_portfolio_2')
def page_general_portfolio_2():
    return render_template('sample_dashboard/page_general_portfolio_2.html')


@sample_dashboard.route('/layout_sidebar_reversed')
def layout_sidebar_reversed():
    return render_template('sample_dashboard/layout_sidebar_reversed.html')


@sample_dashboard.route('/serial_csv')
def serial_csv():
    return render_template('sample_dashboard/serial_csv.html')


@sample_dashboard.route('/pie3')
def pie3():
    return render_template('sample_dashboard/pie3.html')


@sample_dashboard.route('/table_datatables_scroller')
def table_datatables_scroller():
    return render_template('sample_dashboard/table_datatables_scroller.html')


@sample_dashboard.route('/pie4')
def pie4():
    return render_template('sample_dashboard/pie4.html')


@sample_dashboard.route('/background_events')
def background_events():
    return render_template('sample_dashboard/background-events.html')


@sample_dashboard.route('/map_json')
def map_json():
    return render_template('sample_dashboard/map_json.html')


@sample_dashboard.route('/postmessage')
def postmessage():
    return render_template('sample_dashboard/postmessage.html')


@sample_dashboard.route('/china')
def china():
    return render_template('sample_dashboard/china.html')


@sample_dashboard.route('/page_general_help')
def page_general_help():
    return render_template('sample_dashboard/page_general_help.html')


@sample_dashboard.route('/maps_google')
def maps_google():
    return render_template('sample_dashboard/maps_google.html')


@sample_dashboard.route('/serial2_json')
def serial2_json():
    return render_template('sample_dashboard/serial2_json.html')


@sample_dashboard.route('/ui_typography')
def ui_typography():
    return render_template('sample_dashboard/ui_typography.html')


@sample_dashboard.route('/project4')
def project4():
    return render_template('sample_dashboard/project4.html')


@sample_dashboard.route('/components_select2')
def components_select2():
    return render_template('sample_dashboard/components_select2.html')


@sample_dashboard.route('/charts_google')
def charts_google():
    return render_template('sample_dashboard/charts_google.html')


@sample_dashboard.route('/ecommerce_products_edit')
def ecommerce_products_edit():
    return render_template('sample_dashboard/ecommerce_products_edit.html')


@sample_dashboard.route('/page_user_profile_1_account')
def page_user_profile_1_account():
    return render_template('sample_dashboard/page_user_profile_1_account.html')


@sample_dashboard.route('/elements_ribbons')
def elements_ribbons():
    return render_template('sample_dashboard/elements_ribbons.html')


@sample_dashboard.route('/result')
def result():
    return render_template('sample_dashboard/result.html')


@sample_dashboard.route('/page_general_portfolio_1')
def page_general_portfolio_1():
    return render_template('sample_dashboard/page_general_portfolio_1.html')


@sample_dashboard.route('/layout_sidebar_menu_compact')
def layout_sidebar_menu_compact():
    return render_template('sample_dashboard/layout_sidebar_menu_compact.html')


@sample_dashboard.route('/ecommerce_products')
def ecommerce_products():
    return render_template('sample_dashboard/ecommerce_products.html')


@sample_dashboard.route('/table_datatables_editable')
def table_datatables_editable():
    return render_template('sample_dashboard/table_datatables_editable.html')


@sample_dashboard.route('/dst')
def dst():
    return render_template('sample_dashboard/dst.html')


@sample_dashboard.route('/page_system_coming_soon')
def page_system_coming_soon():
    return render_template('sample_dashboard/page_system_coming_soon.html')


@sample_dashboard.route('/table_datatables_responsive')
def table_datatables_responsive():
    return render_template('sample_dashboard/table_datatables_responsive.html')


@sample_dashboard.route('/form_validation')
def form_validation():
    return render_template('sample_dashboard/form_validation.html')


@sample_dashboard.route('/italy')
def italy():
    return render_template('sample_dashboard/italy.html')


@sample_dashboard.route('/uk')
def uk():
    return render_template('sample_dashboard/uk.html')


@sample_dashboard.route('/ui_notific8')
def ui_notific8():
    return render_template('sample_dashboard/ui_notific8.html')


@sample_dashboard.route('/charts_flowchart')
def charts_flowchart():
    return render_template('sample_dashboard/charts_flowchart.html')


@sample_dashboard.route('/json_ld')
def json_ld():
    return render_template('sample_dashboard/json-ld.html')


@sample_dashboard.route('/jquery')
def jquery():
    return render_template('sample_dashboard/jquery.html')


@sample_dashboard.route('/page_general_blog')
def page_general_blog():
    return render_template('sample_dashboard/page_general_blog.html')


@sample_dashboard.route('/layout_blank_page')
def layout_blank_page():
    return render_template('sample_dashboard/layout_blank_page.html')


@sample_dashboard.route('/components_knob_dials')
def components_knob_dials():
    return render_template('sample_dashboard/components_knob_dials.html')


@sample_dashboard.route('/layout_footer_fixed')
def layout_footer_fixed():
    return render_template('sample_dashboard/layout_footer_fixed.html')


@sample_dashboard.route('/components_editors')
def components_editors():
    return render_template('sample_dashboard/components_editors.html')


@sample_dashboard.route('/theme')
def theme():
    return render_template('sample_dashboard/theme.html')


@sample_dashboard.route('/inlinetextarea')
def inlinetextarea():
    return render_template('sample_dashboard/inlinetextarea.html')


@sample_dashboard.route('/charts_highmaps')
def charts_highmaps():
    return render_template('sample_dashboard/charts_highmaps.html')


@sample_dashboard.route('/gauge')
def gauge():
    return render_template('sample_dashboard/gauge.html')


@sample_dashboard.route('/ui_colors')
def ui_colors():
    return render_template('sample_dashboard/ui_colors.html')


@sample_dashboard.route('/years')
def years():
    return render_template('sample_dashboard/years.html')


@sample_dashboard.route('/app_inbox_view')
def app_inbox_view():
    return render_template('sample_dashboard/app_inbox_view.html')


@sample_dashboard.route('/charts_amcharts')
def charts_amcharts():
    return render_template('sample_dashboard/charts_amcharts.html')


@sample_dashboard.route('/uilanguages')
def uilanguages():
    return render_template('sample_dashboard/uilanguages.html')


@sample_dashboard.route('/table_datatables_ajax')
def table_datatables_ajax():
    return render_template('sample_dashboard/table_datatables_ajax.html')


@sample_dashboard.route('/components_ion_sliders')
def components_ion_sliders():
    return render_template('sample_dashboard/components_ion_sliders.html')


@sample_dashboard.route('/portlet_solid')
def portlet_solid():
    return render_template('sample_dashboard/portlet_solid.html')


@sample_dashboard.route('/preview')
def preview():
    return render_template('sample_dashboard/preview.html')


@sample_dashboard.route('/diagonal_xlabels')
def diagonal_xlabels():
    return render_template('sample_dashboard/diagonal-xlabels.html')


@sample_dashboard.route('/project1')
def project1():
    return render_template('sample_dashboard/project1.html')


@sample_dashboard.route('/portlet_ajax_content_3')
def portlet_ajax_content_3():
    return render_template('sample_dashboard/portlet_ajax_content_3.html')


@sample_dashboard.route('/pie1')
def pie1():
    return render_template('sample_dashboard/pie1.html')


@sample_dashboard.route('/app_todo')
def app_todo():
    return render_template('sample_dashboard/app_todo.html')


@sample_dashboard.route('/components_date_time_pickers')
def components_date_time_pickers():
    return render_template('sample_dashboard/components_date_time_pickers.html')


@sample_dashboard.route('/components_color_pickers')
def components_color_pickers():
    return render_template('sample_dashboard/components_color_pickers.html')


@sample_dashboard.route('/pie_csv')
def pie_csv():
    return render_template('sample_dashboard/pie_csv.html')


@sample_dashboard.route('/ui_modals_ajax_sample')
def ui_modals_ajax_sample():
    return render_template('sample_dashboard/ui_modals_ajax_sample.html')


@sample_dashboard.route('/less')
def less():
    return render_template('sample_dashboard/less.html')


@sample_dashboard.route('/enterkey')
def enterkey():
    return render_template('sample_dashboard/enterkey.html')


@sample_dashboard.route('/replacebycode')
def replacebycode():
    return render_template('sample_dashboard/replacebycode.html')


@sample_dashboard.route('/components_noui_sliders')
def components_noui_sliders():
    return render_template('sample_dashboard/components_noui_sliders.html')


@sample_dashboard.route('/components_multi_select')
def components_multi_select():
    return render_template('sample_dashboard/components_multi_select.html')


@sample_dashboard.route('/area')
def area():
    return render_template('sample_dashboard/area.html')


@sample_dashboard.route('/area_as_line')
def area_as_line():
    return render_template('sample_dashboard/area-as-line.html')


@sample_dashboard.route('/page_general_search_2')
def page_general_search_2():
    return render_template('sample_dashboard/page_general_search_2.html')


@sample_dashboard.route('/page_user_login_3')
def page_user_login_3():
    return render_template('sample_dashboard/page_user_login_3.html')


@sample_dashboard.route('/ui_buttons')
def ui_buttons():
    return render_template('sample_dashboard/ui_buttons.html')


@sample_dashboard.route('/scss')
def scss():
    return render_template('sample_dashboard/scss.html')


@sample_dashboard.route('/ui_tabs_accordions_navs')
def ui_tabs_accordions_navs():
    return render_template('sample_dashboard/ui_tabs_accordions_navs.html')


@sample_dashboard.route('/outputforflash')
def outputforflash():
    return render_template('sample_dashboard/outputforflash.html')


@sample_dashboard.route('/gantt')
def gantt():
    return render_template('sample_dashboard/gantt.html')


@sample_dashboard.route('/portlet_ajax_content_error')
def portlet_ajax_content_error():
    return render_template('sample_dashboard/portlet_ajax_content_error.html')


@sample_dashboard.route('/world')
def world():
    return render_template('sample_dashboard/world.html')


@sample_dashboard.route('/page_general_faq')
def page_general_faq():
    return render_template('sample_dashboard/page_general_faq.html')


@sample_dashboard.route('/layout_disabled_menu')
def layout_disabled_menu():
    return render_template('sample_dashboard/layout_disabled_menu.html')


@sample_dashboard.route('/no_grid')
def no_grid():
    return render_template('sample_dashboard/no-grid.html')


@sample_dashboard.route('/page_user_lock_2')
def page_user_lock_2():
    return render_template('sample_dashboard/page_user_lock_2.html')


@sample_dashboard.route('/countdownBasic')
def countdownBasic():
    return render_template('sample_dashboard/countdownBasic.html')


@sample_dashboard.route('/ecommerce_orders_view')
def ecommerce_orders_view():
    return render_template('sample_dashboard/ecommerce_orders_view.html')


@sample_dashboard.route('/ajax')
def ajax():
    return render_template('sample_dashboard/ajax.html')


@sample_dashboard.route('/components_context_menu')
def components_context_menu():
    return render_template('sample_dashboard/components_context_menu.html')


@sample_dashboard.route('/gcal')
def gcal():
    return render_template('sample_dashboard/gcal.html')


@sample_dashboard.route('/russia')
def russia():
    return render_template('sample_dashboard/russia.html')


@sample_dashboard.route('/project2')
def project2():
    return render_template('sample_dashboard/project2.html')


@sample_dashboard.route('/portlet_boxed')
def portlet_boxed():
    return render_template('sample_dashboard/portlet_boxed.html')


@sample_dashboard.route('/page_system_404_1')
def page_system_404_1():
    return render_template('sample_dashboard/page_system_404_1.html')


@sample_dashboard.route('/ui_page_progress_style_2')
def ui_page_progress_style_2():
    return render_template('sample_dashboard/ui_page_progress_style_2.html')


@sample_dashboard.route('/components_typeahead')
def components_typeahead():
    return render_template('sample_dashboard/components_typeahead.html')


@sample_dashboard.route('/portlet_light')
def portlet_light():
    return render_template('sample_dashboard/portlet_light.html')


@sample_dashboard.route('/_template')
def _template():
    return render_template('sample_dashboard/_template.html')


@sample_dashboard.route('/dialog')
def dialog():
    return render_template('sample_dashboard/dialog.html')


@sample_dashboard.route('/components_bootstrap_select_splitter')
def components_bootstrap_select_splitter():
    return render_template('sample_dashboard/components_bootstrap_select_splitter.html')


@sample_dashboard.route('/bar_colors')
def bar_colors():
    return render_template('sample_dashboard/bar-colors.html')


@sample_dashboard.route('/form_validation_md')
def form_validation_md():
    return render_template('sample_dashboard/form_validation_md.html')


@sample_dashboard.route('/ui_general')
def ui_general():
    return render_template('sample_dashboard/ui_general.html')


@sample_dashboard.route('/page_general_search_4')
def page_general_search_4():
    return render_template('sample_dashboard/page_general_search_4.html')


@sample_dashboard.route('/ui_socicons')
def ui_socicons():
    return render_template('sample_dashboard/ui_socicons.html')


@sample_dashboard.route('/donut')
def donut():
    return render_template('sample_dashboard/donut.html')


@sample_dashboard.route('/page_user_login_2')
def page_user_login_2():
    return render_template('sample_dashboard/page_user_login_2.html')


@sample_dashboard.route('/maps_vector')
def maps_vector():
    return render_template('sample_dashboard/maps_vector.html')


@sample_dashboard.route('/page_system_500_2')
def page_system_500_2():
    return render_template('sample_dashboard/page_system_500_2.html')


@sample_dashboard.route('/loadMore')
def loadMore():
    return render_template('sample_dashboard/loadMore.html')


@sample_dashboard.route('/gauge_json')
def gauge_json():
    return render_template('sample_dashboard/gauge_json.html')


@sample_dashboard.route('/page_user_login_6')
def page_user_login_6():
    return render_template('sample_dashboard/page_user_login_6.html')


@sample_dashboard.route('/table_datatables_managed')
def table_datatables_managed():
    return render_template('sample_dashboard/table_datatables_managed.html')


@sample_dashboard.route('/')
def index():
    return render_template('sample_dashboard/index.html')


@sample_dashboard.route('/portlet_ajax_content_1')
def portlet_ajax_content_1():
    return render_template('sample_dashboard/portlet_ajax_content_1.html')


@sample_dashboard.route('/layout_full_height_portlet')
def layout_full_height_portlet():
    return render_template('sample_dashboard/layout_full_height_portlet.html')


@sample_dashboard.route('/ui_bootstrap_growl')
def ui_bootstrap_growl():
    return render_template('sample_dashboard/ui_bootstrap_growl.html')


@sample_dashboard.route('/elements_lists')
def elements_lists():
    return render_template('sample_dashboard/elements_lists.html')


@sample_dashboard.route('/components_bootstrap_switch')
def components_bootstrap_switch():
    return render_template('sample_dashboard/components_bootstrap_switch.html')


@sample_dashboard.route('/table_datatables_colreorder')
def table_datatables_colreorder():
    return render_template('sample_dashboard/table_datatables_colreorder.html')


@sample_dashboard.route('/switzerland')
def switzerland():
    return render_template('sample_dashboard/switzerland.html')


@sample_dashboard.route('/scala')
def scala():
    return render_template('sample_dashboard/scala.html')


@sample_dashboard.route('/test')
def test():
    return render_template('sample_dashboard/test.html')


@sample_dashboard.route('/ui_datepaginator')
def ui_datepaginator():
    return render_template('sample_dashboard/ui_datepaginator.html')


@sample_dashboard.route('/stock')
def stock():
    return render_template('sample_dashboard/stock.html')


@sample_dashboard.route('/charts_echarts')
def charts_echarts():
    return render_template('sample_dashboard/charts_echarts.html')


@sample_dashboard.route('/layout_sidebar_menu_accordion')
def layout_sidebar_menu_accordion():
    return render_template('sample_dashboard/layout_sidebar_menu_accordion.html')


@sample_dashboard.route('/serial1')
def serial1():
    return render_template('sample_dashboard/serial1.html')


@sample_dashboard.route('/france')
def france():
    return render_template('sample_dashboard/france.html')


@sample_dashboard.route('/months_no_smooth')
def months_no_smooth():
    return render_template('sample_dashboard/months-no-smooth.html')


@sample_dashboard.route('/resize')
def resize():
    return render_template('sample_dashboard/resize.html')


@sample_dashboard.route('/app_inbox_compose')
def app_inbox_compose():
    return render_template('sample_dashboard/app_inbox_compose.html')


@sample_dashboard.route('/ui_bootbox')
def ui_bootbox():
    return render_template('sample_dashboard/ui_bootbox.html')


@sample_dashboard.route('/ui_extended_modals_ajax_sample')
def ui_extended_modals_ajax_sample():
    return render_template('sample_dashboard/ui_extended_modals_ajax_sample.html')


@sample_dashboard.route('/app_inbox_reply')
def app_inbox_reply():
    return render_template('sample_dashboard/app_inbox_reply.html')


@sample_dashboard.route('/without_bootstrap')
def without_bootstrap():
    return render_template('sample_dashboard/without-bootstrap.html')


@sample_dashboard.route('/elements_steps')
def elements_steps():
    return render_template('sample_dashboard/elements_steps.html')


@sample_dashboard.route('/page_general_portfolio_4')
def page_general_portfolio_4():
    return render_template('sample_dashboard/page_general_portfolio_4.html')


@sample_dashboard.route('/table_static_responsive')
def table_static_responsive():
    return render_template('sample_dashboard/table_static_responsive.html')


@sample_dashboard.route('/decimal_custom_hover')
def decimal_custom_hover():
    return render_template('sample_dashboard/decimal-custom-hover.html')


@sample_dashboard.route('/ui_extended_modals')
def ui_extended_modals():
    return render_template('sample_dashboard/ui_extended_modals.html')


@sample_dashboard.route('/ui_timeline')
def ui_timeline():
    return render_template('sample_dashboard/ui_timeline.html')


@sample_dashboard.route('/layout_sidebar_fixed')
def layout_sidebar_fixed():
    return render_template('sample_dashboard/layout_sidebar_fixed.html')


@sample_dashboard.route('/page_user_login_5')
def page_user_login_5():
    return render_template('sample_dashboard/page_user_login_5.html')


@sample_dashboard.route('/replacebyclass')
def replacebyclass():
    return render_template('sample_dashboard/replacebyclass.html')


@sample_dashboard.route('/form_controls')
def form_controls():
    return render_template('sample_dashboard/form_controls.html')


@sample_dashboard.route('/layout_language_bar')
def layout_language_bar():
    return render_template('sample_dashboard/layout_language_bar.html')


@sample_dashboard.route('/page_general_blog_post')
def page_general_blog_post():
    return render_template('sample_dashboard/page_general_blog_post.html')


@sample_dashboard.route('/brazil')
def brazil():
    return render_template('sample_dashboard/brazil.html')


@sample_dashboard.route('/page_general_invoice')
def page_general_invoice():
    return render_template('sample_dashboard/page_general_invoice.html')


@sample_dashboard.route('/charts_morris')
def charts_morris():
    return render_template('sample_dashboard/charts_morris.html')


@sample_dashboard.route('/page_general_about')
def page_general_about():
    return render_template('sample_dashboard/page_general_about.html')


@sample_dashboard.route('/page_general_portfolio_3')
def page_general_portfolio_3():
    return render_template('sample_dashboard/page_general_portfolio_3.html')


@sample_dashboard.route('/goals')
def goals():
    return render_template('sample_dashboard/goals.html')


@sample_dashboard.route('/readonly')
def readonly():
    return render_template('sample_dashboard/readonly.html')


@sample_dashboard.route('/diagonal_xlabels_bar')
def diagonal_xlabels_bar():
    return render_template('sample_dashboard/diagonal-xlabels-bar.html')


@sample_dashboard.route('/components_bootstrap_fileinput')
def components_bootstrap_fileinput():
    return render_template('sample_dashboard/components_bootstrap_fileinput.html')


@sample_dashboard.route('/europe')
def europe():
    return render_template('sample_dashboard/europe.html')


@sample_dashboard.route('/pie2')
def pie2():
    return render_template('sample_dashboard/pie2.html')


@sample_dashboard.route('/page_general_pricing_2')
def page_general_pricing_2():
    return render_template('sample_dashboard/page_general_pricing_2.html')


@sample_dashboard.route('/page_user_lock_1')
def page_user_lock_1():
    return render_template('sample_dashboard/page_user_lock_1.html')


@sample_dashboard.route('/datafiltering')
def datafiltering():
    return render_template('sample_dashboard/datafiltering.html')


@sample_dashboard.route('/apartment')
def apartment():
    return render_template('sample_dashboard/apartment.html')


@sample_dashboard.route('/form_editable')
def form_editable():
    return render_template('sample_dashboard/form_editable.html')


@sample_dashboard.route('/australia')
def australia():
    return render_template('sample_dashboard/australia.html')


@sample_dashboard.route('/non_date')
def non_date():
    return render_template('sample_dashboard/non-date.html')


@sample_dashboard.route('/weeks')
def weeks():
    return render_template('sample_dashboard/weeks.html')


@sample_dashboard.route('/table_static_basic')
def table_static_basic():
    return render_template('sample_dashboard/table_static_basic.html')


@sample_dashboard.route('/ui_tree')
def ui_tree():
    return render_template('sample_dashboard/ui_tree.html')


@sample_dashboard.route('/dashboard_2')
def dashboard_2():
    return render_template('sample_dashboard/dashboard_2.html')


@sample_dashboard.route('/ui_icons')
def ui_icons():
    return render_template('sample_dashboard/ui_icons.html')


@sample_dashboard.route('/charts_highstock')
def charts_highstock():
    return render_template('sample_dashboard/charts_highstock.html')


@sample_dashboard.route('/xy')
def xy():
    return render_template('sample_dashboard/xy.html')


@sample_dashboard.route('/layout_sidebar_closed')
def layout_sidebar_closed():
    return render_template('sample_dashboard/layout_sidebar_closed.html')


@sample_dashboard.route('/negative')
def negative():
    return render_template('sample_dashboard/negative.html')


@sample_dashboard.route('/components_bootstrap_maxlength')
def components_bootstrap_maxlength():
    return render_template('sample_dashboard/components_bootstrap_maxlength.html')


@sample_dashboard.route('/magicline')
def magicline():
    return render_template('sample_dashboard/magicline.html')


@sample_dashboard.route('/loadMore3')
def loadMore3():
    return render_template('sample_dashboard/loadMore3.html')


@sample_dashboard.route('/funnel')
def funnel():
    return render_template('sample_dashboard/funnel.html')


@sample_dashboard.route('/page_system_500_1')
def page_system_500_1():
    return render_template('sample_dashboard/page_system_500_1.html')


@sample_dashboard.route('/page_user_login_4')
def page_user_login_4():
    return render_template('sample_dashboard/page_user_login_4.html')


@sample_dashboard.route('/page_general_search_5')
def page_general_search_5():
    return render_template('sample_dashboard/page_general_search_5.html')


@sample_dashboard.route('/page_general_search')
def page_general_search():
    return render_template('sample_dashboard/page_general_search.html')


@sample_dashboard.route('/ecommerce_index')
def ecommerce_index():
    return render_template('sample_dashboard/ecommerce_index.html')


@sample_dashboard.route('/page_general_invoice_2')
def page_general_invoice_2():
    return render_template('sample_dashboard/page_general_invoice_2.html')


@sample_dashboard.route('/events')
def events():
    return render_template('sample_dashboard/events.html')


@sample_dashboard.route('/typescript')
def typescript():
    return render_template('sample_dashboard/typescript.html')


@sample_dashboard.route('/loadMore4')
def loadMore4():
    return render_template('sample_dashboard/loadMore4.html')


@sample_dashboard.route('/ecommerce_orders')
def ecommerce_orders():
    return render_template('sample_dashboard/ecommerce_orders.html')


@sample_dashboard.route('/charts_flotcharts')
def charts_flotcharts():
    return render_template('sample_dashboard/charts_flotcharts.html')


@sample_dashboard.route('/languages')
def languages():
    return render_template('sample_dashboard/languages.html')


@sample_dashboard.route('/layout_boxed_page')
def layout_boxed_page():
    return render_template('sample_dashboard/layout_boxed_page.html')


@sample_dashboard.route('/selectable')
def selectable():
    return render_template('sample_dashboard/selectable.html')


@sample_dashboard.route('/timestamps')
def timestamps():
    return render_template('sample_dashboard/timestamps.html')


@sample_dashboard.route('/usa')
def usa():
    return render_template('sample_dashboard/usa.html')


@sample_dashboard.route('/components_bootstrap_select')
def components_bootstrap_select():
    return render_template('sample_dashboard/components_bootstrap_select.html')


@sample_dashboard.route('/donut_formatter')
def donut_formatter():
    return render_template('sample_dashboard/donut-formatter.html')


@sample_dashboard.route('/page_user_profile_2')
def page_user_profile_2():
    return render_template('sample_dashboard/page_user_profile_2.html')


@sample_dashboard.route('/dashboard_3')
def dashboard_3():
    return render_template('sample_dashboard/dashboard_3.html')


@sample_dashboard.route('/api')
def api():
    return render_template('sample_dashboard/api.html')


@sample_dashboard.route('/serial3')
def serial3():
    return render_template('sample_dashboard/serial3.html')


@sample_dashboard.route('/components_form_tools')
def components_form_tools():
    return render_template('sample_dashboard/components_form_tools.html')


@sample_dashboard.route('/page_system_404_3')
def page_system_404_3():
    return render_template('sample_dashboard/page_system_404_3.html')


@sample_dashboard.route('/components_bootstrap_touchspin')
def components_bootstrap_touchspin():
    return render_template('sample_dashboard/components_bootstrap_touchspin.html')

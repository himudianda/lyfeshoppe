from flask import Blueprint, render_template

sample_frontend = Blueprint('sample_frontend', __name__, template_folder='templates')


@sample_frontend.route('/blog_masonry_full')
def blog_masonry_full():
    return render_template('sample_frontend/blog-masonry-full.html')


@sample_frontend.route('/full_width')
def full_width():
    return render_template('sample_frontend/full-width.html')


@sample_frontend.route('/custom_calendar')
def custom_calendar():
    return render_template('sample_frontend/custom-calendar.html')


@sample_frontend.route('/index_portfolio')
def index_portfolio():
    return render_template('sample_frontend/index-portfolio.html')


@sample_frontend.route('/page_title_gmap_mini')
def page_title_gmap_mini():
    return render_template('sample_frontend/page-title-gmap-mini.html')


@sample_frontend.route('/portfolio_right_sidebar')
def portfolio_right_sidebar():
    return render_template('sample_frontend/portfolio-right-sidebar.html')


@sample_frontend.route('/header_side_left_open')
def header_side_left_open():
    return render_template('sample_frontend/header-side-left-open.html')


@sample_frontend.route('/portfolio_fullwidth')
def portfolio_fullwidth():
    return render_template('sample_frontend/portfolio-fullwidth.html')


@sample_frontend.route('/blog_single')
def blog_single():
    return render_template('sample_frontend/blog-single.html')


@sample_frontend.route('/blog_left_sidebar')
def blog_left_sidebar():
    return render_template('sample_frontend/blog-left-sidebar.html')


@sample_frontend.route('/event_single_both_sidebar')
def event_single_both_sidebar():
    return render_template('sample_frontend/event-single-both-sidebar.html')


@sample_frontend.route('/modal_onload_cookie')
def modal_onload_cookie():
    return render_template('sample_frontend/modal-onload-cookie.html')


@sample_frontend.route('/cookies')
def cookies():
    return render_template('sample_frontend/cookies.html')


@sample_frontend.route('/menu_10')
def menu_10():
    return render_template('sample_frontend/menu-10.html')


@sample_frontend.route('/combination_filter_bt_dropdown')
def combination_filter_bt_dropdown():
    return render_template('sample_frontend/combination-filter-bt-dropdown.html')


@sample_frontend.route('/slider_owl')
def slider_owl():
    return render_template('sample_frontend/slider-owl.html')


@sample_frontend.route('/pagination_progress')
def pagination_progress():
    return render_template('sample_frontend/pagination-progress.html')


@sample_frontend.route('/style_boxes')
def style_boxes():
    return render_template('sample_frontend/style-boxes.html')


@sample_frontend.route('/portfolio_masonry_right_sidebar')
def portfolio_masonry_right_sidebar():
    return render_template('sample_frontend/portfolio-masonry-right-sidebar.html')


@sample_frontend.route('/portfolio_3_masonry')
def portfolio_3_masonry():
    return render_template('sample_frontend/portfolio-3-masonry.html')


@sample_frontend.route('/styled_icons')
def styled_icons():
    return render_template('sample_frontend/styled-icons.html')


@sample_frontend.route('/portfolio_2_masonry')
def portfolio_2_masonry():
    return render_template('sample_frontend/portfolio-2-masonry.html')


@sample_frontend.route('/portfolio_single_thumbs_left_sidebar')
def portfolio_single_thumbs_left_sidebar():
    return render_template('sample_frontend/portfolio-single-thumbs-left-sidebar.html')


@sample_frontend.route('/cart')
def cart():
    return render_template('sample_frontend/cart.html')


@sample_frontend.route('/intro')
def intro():
    return render_template('sample_frontend/intro.html')


@sample_frontend.route('/login_register_2')
def login_register_2():
    return render_template('sample_frontend/login-register-2.html')


@sample_frontend.route('/shop_2_right_sidebar')
def shop_2_right_sidebar():
    return render_template('sample_frontend/shop-2-right-sidebar.html')


@sample_frontend.route('/shop_1_left_sidebar')
def shop_1_left_sidebar():
    return render_template('sample_frontend/shop-1-left-sidebar.html')


@sample_frontend.route('/blog_grid_2_left_sidebar')
def blog_grid_2_left_sidebar():
    return render_template('sample_frontend/blog-grid-2-left-sidebar.html')


@sample_frontend.route('/blog_single_full')
def blog_single_full():
    return render_template('sample_frontend/blog-single-full.html')


@sample_frontend.route('/blog_grid_3_left_sidebar')
def blog_grid_3_left_sidebar():
    return render_template('sample_frontend/blog-grid-3-left-sidebar.html')


@sample_frontend.route('/portfolio_single_thumbs_fullwidth')
def portfolio_single_thumbs_fullwidth():
    return render_template('sample_frontend/portfolio-single-thumbs-fullwidth.html')


@sample_frontend.route('/portfolio_single_video_right')
def portfolio_single_video_right():
    return render_template('sample_frontend/portfolio-single-video-right.html')


@sample_frontend.route('/pricing')
def pricing():
    return render_template('sample_frontend/pricing.html')


@sample_frontend.route('/event_single_full_width_image')
def event_single_full_width_image():
    return render_template('sample_frontend/event-single-full-width-image.html')


@sample_frontend.route('/login_2')
def login_2():
    return render_template('sample_frontend/login-2.html')


@sample_frontend.route('/portfolio_masonry_left_sidebar')
def portfolio_masonry_left_sidebar():
    return render_template('sample_frontend/portfolio-masonry-left-sidebar.html')


@sample_frontend.route('/portfolio_notitle_left_sidebar')
def portfolio_notitle_left_sidebar():
    return render_template('sample_frontend/portfolio-notitle-left-sidebar.html')


@sample_frontend.route('/footer_3')
def footer_3():
    return render_template('sample_frontend/footer-3.html')


@sample_frontend.route('/portfolio_single_video_full')
def portfolio_single_video_full():
    return render_template('sample_frontend/portfolio-single-video-full.html')


@sample_frontend.route('/terms')
def terms():
    return render_template('sample_frontend/terms.html')


@sample_frontend.route('/footer_6')
def footer_6():
    return render_template('sample_frontend/footer-6.html')


@sample_frontend.route('/charts')
def charts():
    return render_template('sample_frontend/charts.html')


@sample_frontend.route('/like_button_in_footer')
def like_button_in_footer():
    return render_template('sample_frontend/like-button-in-footer.html')


@sample_frontend.route('/page_title_pattern')
def page_title_pattern():
    return render_template('sample_frontend/page-title-pattern.html')


@sample_frontend.route('/coming_soon_2')
def coming_soon_2():
    return render_template('sample_frontend/coming-soon-2.html')


@sample_frontend.route('/portfolio_single_video_fullwidth_both_sidebar')
def portfolio_single_video_fullwidth_both_sidebar():
    return render_template('sample_frontend/portfolio-single-video-fullwidth-both-sidebar.html')


@sample_frontend.route('/slider_owl_videos')
def slider_owl_videos():
    return render_template('sample_frontend/slider-owl-videos.html')


@sample_frontend.route('/portfolio_5_nomargin_left_sidebar')
def portfolio_5_nomargin_left_sidebar():
    return render_template('sample_frontend/portfolio-5-nomargin-left-sidebar.html')


@sample_frontend.route('/portfolio_5_masonry_nomargin')
def portfolio_5_masonry_nomargin():
    return render_template('sample_frontend/portfolio-5-masonry-nomargin.html')


@sample_frontend.route('/pie_skills')
def pie_skills():
    return render_template('sample_frontend/pie-skills.html')


@sample_frontend.route('/portfolio_1_both_sidebar')
def portfolio_1_both_sidebar():
    return render_template('sample_frontend/portfolio-1-both-sidebar.html')


@sample_frontend.route('/blog_grid_3_right_sidebar')
def blog_grid_3_right_sidebar():
    return render_template('sample_frontend/blog-grid-3-right-sidebar.html')


@sample_frontend.route('/preloaders')
def preloaders():
    return render_template('sample_frontend/preloaders.html')


@sample_frontend.route('/subscribe_with_name')
def subscribe_with_name():
    return render_template('sample_frontend/subscribe-with-name.html')


@sample_frontend.route('/portfolio_2_notitle_both_sidebar')
def portfolio_2_notitle_both_sidebar():
    return render_template('sample_frontend/portfolio-2-notitle-both-sidebar.html')


@sample_frontend.route('/portfolio_masonry_both_sidebar')
def portfolio_masonry_both_sidebar():
    return render_template('sample_frontend/portfolio-masonry-both-sidebar.html')


@sample_frontend.route('/faqs_3')
def faqs_3():
    return render_template('sample_frontend/faqs-3.html')


@sample_frontend.route('/toggles_accordions')
def toggles_accordions():
    return render_template('sample_frontend/toggles-accordions.html')


@sample_frontend.route('/lightbox')
def lightbox():
    return render_template('sample_frontend/lightbox.html')


@sample_frontend.route('/static_thumbs_grid')
def static_thumbs_grid():
    return render_template('sample_frontend/static-thumbs-grid.html')


@sample_frontend.route('/page_title_mini')
def page_title_mini():
    return render_template('sample_frontend/page-title-mini.html')


@sample_frontend.route('/responsive_class')
def responsive_class():
    return render_template('sample_frontend/responsive-class.html')


@sample_frontend.route('/counters')
def counters():
    return render_template('sample_frontend/counters.html')


@sample_frontend.route('/flex_with_carousel_thumbs')
def flex_with_carousel_thumbs():
    return render_template('sample_frontend/flex-with-carousel-thumbs.html')


@sample_frontend.route('/index_wedding')
def index_wedding():
    return render_template('sample_frontend/index-wedding.html')


@sample_frontend.route('/portfolio_single_left_sidebar')
def portfolio_single_left_sidebar():
    return render_template('sample_frontend/portfolio-single-left-sidebar.html')


@sample_frontend.route('/index_magazine_2')
def index_magazine_2():
    return render_template('sample_frontend/index-magazine-2.html')


@sample_frontend.route('/menu_with_button')
def menu_with_button():
    return render_template('sample_frontend/menu-with-button.html')


@sample_frontend.route('/portfolio_5_masonry_title_overlay')
def portfolio_5_masonry_title_overlay():
    return render_template('sample_frontend/portfolio-5-masonry-title-overlay.html')


@sample_frontend.route('/menu_with_image')
def menu_with_image():
    return render_template('sample_frontend/menu-with-image.html')


@sample_frontend.route('/portfolio_3_masonry_left_sidebar')
def portfolio_3_masonry_left_sidebar():
    return render_template('sample_frontend/portfolio-3-masonry-left-sidebar.html')


@sample_frontend.route('/index_shop')
def index_shop():
    return render_template('sample_frontend/index-shop.html')


@sample_frontend.route('/faqs_2')
def faqs_2():
    return render_template('sample_frontend/faqs-2.html')


@sample_frontend.route('/static_parallax')
def static_parallax():
    return render_template('sample_frontend/static-parallax.html')


@sample_frontend.route('/blog_grid_2')
def blog_grid_2():
    return render_template('sample_frontend/blog-grid-2.html')


@sample_frontend.route('/landing')
def landing():
    return render_template('sample_frontend/landing.html')


@sample_frontend.route('/portfolio_6_fullwidth_notitle')
def portfolio_6_fullwidth_notitle():
    return render_template('sample_frontend/portfolio-6-fullwidth-notitle.html')


@sample_frontend.route('/blog_small_full_width')
def blog_small_full_width():
    return render_template('sample_frontend/blog-small-full-width.html')


@sample_frontend.route('/blog_grid_2_right_sidebar')
def blog_grid_2_right_sidebar():
    return render_template('sample_frontend/blog-grid-2-right-sidebar.html')


@sample_frontend.route('/menu_4')
def menu_4():
    return render_template('sample_frontend/menu-4.html')


@sample_frontend.route('/dividers')
def dividers():
    return render_template('sample_frontend/dividers.html')


@sample_frontend.route('/demo_construction')
def demo_construction():
    return render_template('sample_frontend/demo-construction.html')


@sample_frontend.route('/footer_5')
def footer_5():
    return render_template('sample_frontend/footer-5.html')


@sample_frontend.route('/page_title_right')
def page_title_right():
    return render_template('sample_frontend/page-title-right.html')


@sample_frontend.route('/blog_small_alt')
def blog_small_alt():
    return render_template('sample_frontend/blog-small-alt.html')


@sample_frontend.route('/shop_2_both_sidebar')
def shop_2_both_sidebar():
    return render_template('sample_frontend/shop-2-both-sidebar.html')


@sample_frontend.route('/portfolio_1_full_both_sidebar')
def portfolio_1_full_both_sidebar():
    return render_template('sample_frontend/portfolio-1-full-both-sidebar.html')


@sample_frontend.route('/portfolio_left_sidebar')
def portfolio_left_sidebar():
    return render_template('sample_frontend/portfolio-left-sidebar.html')


@sample_frontend.route('/portfolio_single_extended')
def portfolio_single_extended():
    return render_template('sample_frontend/portfolio-single-extended.html')


@sample_frontend.route('/portfolio_single_fullwidth_both_sidebar')
def portfolio_single_fullwidth_both_sidebar():
    return render_template('sample_frontend/portfolio-single-fullwidth-both-sidebar.html')


@sample_frontend.route('/index_fullscreen_image')
def index_fullscreen_image():
    return render_template('sample_frontend/index-fullscreen-image.html')


@sample_frontend.route('/header_side_right')
def header_side_right():
    return render_template('sample_frontend/header-side-right.html')


@sample_frontend.route('/blog_timeline_left_sidebar')
def blog_timeline_left_sidebar():
    return render_template('sample_frontend/blog-timeline-left-sidebar.html')


@sample_frontend.route('/page_title_center')
def page_title_center():
    return render_template('sample_frontend/page-title-center.html')


@sample_frontend.route('/slider_revolution_fullwidth')
def slider_revolution_fullwidth():
    return render_template('sample_frontend/slider-revolution-fullwidth.html')


@sample_frontend.route('/portfolio_jpagination')
def portfolio_jpagination():
    return render_template('sample_frontend/portfolio-jpagination.html')


@sample_frontend.route('/portfolio_3_notitle_right_sidebar')
def portfolio_3_notitle_right_sidebar():
    return render_template('sample_frontend/portfolio-3-notitle-right-sidebar.html')


@sample_frontend.route('/portfolio_masonry_title_overlay')
def portfolio_masonry_title_overlay():
    return render_template('sample_frontend/portfolio-masonry-title-overlay.html')


@sample_frontend.route('/index_onepage_2')
def index_onepage_2():
    return render_template('sample_frontend/index-onepage-2.html')


@sample_frontend.route('/landing_4')
def landing_4():
    return render_template('sample_frontend/landing-4.html')


@sample_frontend.route('/portfolio_2_masonry_right_sidebar')
def portfolio_2_masonry_right_sidebar():
    return render_template('sample_frontend/portfolio-2-masonry-right-sidebar.html')


@sample_frontend.route('/widgets')
def widgets():
    return render_template('sample_frontend/widgets.html')


@sample_frontend.route('/portfolio_3_masonry_both_sidebar')
def portfolio_3_masonry_both_sidebar():
    return render_template('sample_frontend/portfolio-3-masonry-both-sidebar.html')


@sample_frontend.route('/header_side_left')
def header_side_left():
    return render_template('sample_frontend/header-side-left.html')


@sample_frontend.route('/event_single_full_width_map')
def event_single_full_width_map():
    return render_template('sample_frontend/event-single-full-width-map.html')


@sample_frontend.route('/index_portfolio_4')
def index_portfolio_4():
    return render_template('sample_frontend/index-portfolio-4.html')


@sample_frontend.route('/portfolio_6')
def portfolio_6():
    return render_template('sample_frontend/portfolio-6.html')


@sample_frontend.route('/shop_1_both_sidebar')
def shop_1_both_sidebar():
    return render_template('sample_frontend/shop-1-both-sidebar.html')


@sample_frontend.route('/index_blog_3')
def index_blog_3():
    return render_template('sample_frontend/index-blog-3.html')


@sample_frontend.route('/portfolio_nomargin_left_sidebar')
def portfolio_nomargin_left_sidebar():
    return render_template('sample_frontend/portfolio-nomargin-left-sidebar.html')


@sample_frontend.route('/menu_7_navbar')
def menu_7_navbar():
    return render_template('sample_frontend/menu-7-navbar.html')


@sample_frontend.route('/portfolio_3_fullwidth')
def portfolio_3_fullwidth():
    return render_template('sample_frontend/portfolio-3-fullwidth.html')


@sample_frontend.route('/portfolio_2_masonry_title_overlay')
def portfolio_2_masonry_title_overlay():
    return render_template('sample_frontend/portfolio-2-masonry-title-overlay.html')


@sample_frontend.route('/portfolio_2_title_overlay')
def portfolio_2_title_overlay():
    return render_template('sample_frontend/portfolio-2-title-overlay.html')


@sample_frontend.route('/generate')
def generate():
    return render_template('sample_frontend/generate.html')


@sample_frontend.route('/slider_carousel_thumbs')
def slider_carousel_thumbs():
    return render_template('sample_frontend/slider-carousel-thumbs.html')


@sample_frontend.route('/portfolio_1_full_right_sidebar')
def portfolio_1_full_right_sidebar():
    return render_template('sample_frontend/portfolio-1-full-right-sidebar.html')


@sample_frontend.route('/header_semi_transparent_dark')
def header_semi_transparent_dark():
    return render_template('sample_frontend/header-semi-transparent-dark.html')


@sample_frontend.route('/portfolio_6_masonry')
def portfolio_6_masonry():
    return render_template('sample_frontend/portfolio-6-masonry.html')


@sample_frontend.route('/portfolio_3_fullwidth_masonry')
def portfolio_3_fullwidth_masonry():
    return render_template('sample_frontend/portfolio-3-fullwidth-masonry.html')


@sample_frontend.route('/blog_small')
def blog_small():
    return render_template('sample_frontend/blog-small.html')


@sample_frontend.route('/portfolio_fullwidth_masonry')
def portfolio_fullwidth_masonry():
    return render_template('sample_frontend/portfolio-fullwidth-masonry.html')


@sample_frontend.route('/landing_2')
def landing_2():
    return render_template('sample_frontend/landing-2.html')


@sample_frontend.route('/portfolio_3_masonry_right_sidebar')
def portfolio_3_masonry_right_sidebar():
    return render_template('sample_frontend/portfolio-3-masonry-right-sidebar.html')


@sample_frontend.route('/portfolio_6_title_overlay')
def portfolio_6_title_overlay():
    return render_template('sample_frontend/portfolio-6-title-overlay.html')


@sample_frontend.route('/blog_masonry_2_both_sidebar')
def blog_masonry_2_both_sidebar():
    return render_template('sample_frontend/blog-masonry-2-both-sidebar.html')


@sample_frontend.route('/slider_elastic')
def slider_elastic():
    return render_template('sample_frontend/slider-elastic.html')


@sample_frontend.route('/sitemap')
def sitemap():
    return render_template('sample_frontend/sitemap.html')


@sample_frontend.route('/portfolio_horizontal_filter')
def portfolio_horizontal_filter():
    return render_template('sample_frontend/portfolio-horizontal-filter.html')


@sample_frontend.route('/index_blog')
def index_blog():
    return render_template('sample_frontend/index-blog.html')


@sample_frontend.route('/portfolio_1_full_alt')
def portfolio_1_full_alt():
    return render_template('sample_frontend/portfolio-1-full-alt.html')


@sample_frontend.route('/portfolio_single_fullwidth_right_sidebar')
def portfolio_single_fullwidth_right_sidebar():
    return render_template('sample_frontend/portfolio-single-fullwidth-right-sidebar.html')


@sample_frontend.route('/events_list_parallax')
def events_list_parallax():
    return render_template('sample_frontend/events-list-parallax.html')


@sample_frontend.route('/portfolio_fullwidth_notitle')
def portfolio_fullwidth_notitle():
    return render_template('sample_frontend/portfolio-fullwidth-notitle.html')


@sample_frontend.route('/portfolio_single_thumbs_fullwidth_right_sidebar')
def portfolio_single_thumbs_fullwidth_right_sidebar():
    return render_template('sample_frontend/portfolio-single-thumbs-fullwidth-right-sidebar.html')


@sample_frontend.route('/portfolio_single_gallery_full')
def portfolio_single_gallery_full():
    return render_template('sample_frontend/portfolio-single-gallery-full.html')


@sample_frontend.route('/index_blog_2')
def index_blog_2():
    return render_template('sample_frontend/index-blog-2.html')


@sample_frontend.route('/menu_6')
def menu_6():
    return render_template('sample_frontend/menu-6.html')


@sample_frontend.route('/index_magazine')
def index_magazine():
    return render_template('sample_frontend/index-magazine.html')


@sample_frontend.route('/events_list_left_sidebar')
def events_list_left_sidebar():
    return render_template('sample_frontend/events-list-left-sidebar.html')


@sample_frontend.route('/portfolio_2_right_sidebar')
def portfolio_2_right_sidebar():
    return render_template('sample_frontend/portfolio-2-right-sidebar.html')


@sample_frontend.route('/portfolio_2_masonry_nomargin')
def portfolio_2_masonry_nomargin():
    return render_template('sample_frontend/portfolio-2-masonry-nomargin.html')


@sample_frontend.route('/blog_grid_2_both_sidebar')
def blog_grid_2_both_sidebar():
    return render_template('sample_frontend/blog-grid-2-both-sidebar.html')


@sample_frontend.route('/index_app_showcase')
def index_app_showcase():
    return render_template('sample_frontend/index-app-showcase.html')


@sample_frontend.route('/icon_lists')
def icon_lists():
    return render_template('sample_frontend/icon-lists.html')


@sample_frontend.route('/portfolio_6_fullwidth_masonry')
def portfolio_6_fullwidth_masonry():
    return render_template('sample_frontend/portfolio-6-fullwidth-masonry.html')


@sample_frontend.route('/index_onepage_3')
def index_onepage_3():
    return render_template('sample_frontend/index-onepage-3.html')


@sample_frontend.route('/blog_single_small_both_sidebar')
def blog_single_small_both_sidebar():
    return render_template('sample_frontend/blog-single-small-both-sidebar.html')


@sample_frontend.route('/slider_camera')
def slider_camera():
    return render_template('sample_frontend/slider-camera.html')


@sample_frontend.route('/events_list_both_sidebar')
def events_list_both_sidebar():
    return render_template('sample_frontend/events-list-both-sidebar.html')


@sample_frontend.route('/index_magazine_3')
def index_magazine_3():
    return render_template('sample_frontend/index-magazine-3.html')


@sample_frontend.route('/blog_both_sidebar')
def blog_both_sidebar():
    return render_template('sample_frontend/blog-both-sidebar.html')


@sample_frontend.route('/index_corporate_2')
def index_corporate_2():
    return render_template('sample_frontend/index-corporate-2.html')


@sample_frontend.route('/portfolio_single_image_right')
def portfolio_single_image_right():
    return render_template('sample_frontend/portfolio-single-image-right.html')


@sample_frontend.route('/portfolio_5_fullwidth_masonry')
def portfolio_5_fullwidth_masonry():
    return render_template('sample_frontend/portfolio-5-fullwidth-masonry.html')


@sample_frontend.route('/modal_onload_iframe')
def modal_onload_iframe():
    return render_template('sample_frontend/modal-onload-iframe.html')


@sample_frontend.route('/contact_7')
def contact_7():
    return render_template('sample_frontend/contact-7.html')


@sample_frontend.route('/portfolio_2_nomargin')
def portfolio_2_nomargin():
    return render_template('sample_frontend/portfolio-2-nomargin.html')


@sample_frontend.route('/events_list')
def events_list():
    return render_template('sample_frontend/events-list.html')


@sample_frontend.route('/header_transparent')
def header_transparent():
    return render_template('sample_frontend/header-transparent.html')


@sample_frontend.route('/404_2')
def 404_2():
    return render_template('sample_frontend/404-2.html')


@sample_frontend.route('/footer_4')
def footer_4():
    return render_template('sample_frontend/footer-4.html')


@sample_frontend.route('/blog_single_small')
def blog_single_small():
    return render_template('sample_frontend/blog-single-small.html')


@sample_frontend.route('/portfolio_2_nomargin_both_sidebar')
def portfolio_2_nomargin_both_sidebar():
    return render_template('sample_frontend/portfolio-2-nomargin-both-sidebar.html')


@sample_frontend.route('/carousel_filter')
def carousel_filter():
    return render_template('sample_frontend/carousel-filter.html')


@sample_frontend.route('/portfolio_3_nomargin_both_sidebar')
def portfolio_3_nomargin_both_sidebar():
    return render_template('sample_frontend/portfolio-3-nomargin-both-sidebar.html')


@sample_frontend.route('/shop_single_custom_linking')
def shop_single_custom_linking():
    return render_template('sample_frontend/shop-single-custom-linking.html')


@sample_frontend.route('/portfolio_single_gallery_fullwidth_right_sidebar')
def portfolio_single_gallery_fullwidth_right_sidebar():
    return render_template('sample_frontend/portfolio-single-gallery-fullwidth-right-sidebar.html')


@sample_frontend.route('/shop_single_custom_linking_carousel')
def shop_single_custom_linking_carousel():
    return render_template('sample_frontend/shop-single-custom-linking-carousel.html')


@sample_frontend.route('/portfolio_single_fullwidth_left_sidebar')
def portfolio_single_fullwidth_left_sidebar():
    return render_template('sample_frontend/portfolio-single-fullwidth-left-sidebar.html')


@sample_frontend.route('/blog_single_both_sidebar')
def blog_single_both_sidebar():
    return render_template('sample_frontend/blog-single-both-sidebar.html')


@sample_frontend.route('/header_dark')
def header_dark():
    return render_template('sample_frontend/header-dark.html')


@sample_frontend.route('/maintenance')
def maintenance():
    return render_template('sample_frontend/maintenance.html')


@sample_frontend.route('/event_single_full_width_slider')
def event_single_full_width_slider():
    return render_template('sample_frontend/event-single-full-width-slider.html')


@sample_frontend.route('/logo_changer')
def logo_changer():
    return render_template('sample_frontend/logo-changer.html')


@sample_frontend.route('/slider_cheermonk_fade')
def slider_cheermonk_fade():
    return render_template('sample_frontend/slider-cheermonk-fade.html')


@sample_frontend.route('/header_side_left_open_push')
def header_side_left_open_push():
    return render_template('sample_frontend/header-side-left-open-push.html')


@sample_frontend.route('/blog_small_both_sidebar')
def blog_small_both_sidebar():
    return render_template('sample_frontend/blog-small-both-sidebar.html')


@sample_frontend.route('/portfolio_single_full')
def portfolio_single_full():
    return render_template('sample_frontend/portfolio-single-full.html')


@sample_frontend.route('/contact_2')
def contact_2():
    return render_template('sample_frontend/contact-2.html')


@sample_frontend.route('/media_embeds')
def media_embeds():
    return render_template('sample_frontend/media-embeds.html')


@sample_frontend.route('/blank_page')
def blank_page():
    return render_template('sample_frontend/blank-page.html')


@sample_frontend.route('/portfolio_single_gallery_fullwidth')
def portfolio_single_gallery_fullwidth():
    return render_template('sample_frontend/portfolio-single-gallery-fullwidth.html')


@sample_frontend.route('/portfolio_1')
def portfolio_1():
    return render_template('sample_frontend/portfolio-1.html')


@sample_frontend.route('/portfolio_5')
def portfolio_5():
    return render_template('sample_frontend/portfolio-5.html')


@sample_frontend.route('/modal_onload_subscribe')
def modal_onload_subscribe():
    return render_template('sample_frontend/modal-onload-subscribe.html')


@sample_frontend.route('/right_sidebar')
def right_sidebar():
    return render_template('sample_frontend/right-sidebar.html')


@sample_frontend.route('/combination_filter_links')
def combination_filter_links():
    return render_template('sample_frontend/combination-filter-links.html')


@sample_frontend.route('/contact_5')
def contact_5():
    return render_template('sample_frontend/contact-5.html')


@sample_frontend.route('/portfolio_nomargin_right_sidebar')
def portfolio_nomargin_right_sidebar():
    return render_template('sample_frontend/portfolio-nomargin-right-sidebar.html')


@sample_frontend.route('/portfolio_single_both_sidebar')
def portfolio_single_both_sidebar():
    return render_template('sample_frontend/portfolio-single-both-sidebar.html')


@sample_frontend.route('/blog_single_split_right_sidebar')
def blog_single_split_right_sidebar():
    return render_template('sample_frontend/blog-single-split-right-sidebar.html')


@sample_frontend.route('/portfolio_infinity_scroll')
def portfolio_infinity_scroll():
    return render_template('sample_frontend/portfolio-infinity-scroll.html')


@sample_frontend.route('/responsive_sticky')
def responsive_sticky():
    return render_template('sample_frontend/responsive-sticky.html')


@sample_frontend.route('/blog_masonry_3')
def blog_masonry_3():
    return render_template('sample_frontend/blog-masonry-3.html')


@sample_frontend.route('/portfolio_3_nomargin')
def portfolio_3_nomargin():
    return render_template('sample_frontend/portfolio-3-nomargin.html')


@sample_frontend.route('/static_sticky')
def static_sticky():
    return render_template('sample_frontend/static-sticky.html')


@sample_frontend.route('/blog_grid')
def blog_grid():
    return render_template('sample_frontend/blog-grid.html')


@sample_frontend.route('/portfolio_2_notitle_left_sidebar')
def portfolio_2_notitle_left_sidebar():
    return render_template('sample_frontend/portfolio-2-notitle-left-sidebar.html')


@sample_frontend.route('/blog_single_left_sidebar')
def blog_single_left_sidebar():
    return render_template('sample_frontend/blog-single-left-sidebar.html')


@sample_frontend.route('/menu_11')
def menu_11():
    return render_template('sample_frontend/menu-11.html')


@sample_frontend.route('/portfolio_1_alt_right_sidebar')
def portfolio_1_alt_right_sidebar():
    return render_template('sample_frontend/portfolio-1-alt-right-sidebar.html')


@sample_frontend.route('/slider_owl_full')
def slider_owl_full():
    return render_template('sample_frontend/slider-owl-full.html')


@sample_frontend.route('/portfolio_3')
def portfolio_3():
    return render_template('sample_frontend/portfolio-3.html')


@sample_frontend.route('/blog_masonry_2')
def blog_masonry_2():
    return render_template('sample_frontend/blog-masonry-2.html')


@sample_frontend.route('/portfolio_masonry_nomargin')
def portfolio_masonry_nomargin():
    return render_template('sample_frontend/portfolio-masonry-nomargin.html')


@sample_frontend.route('/portfolio_5_notitle')
def portfolio_5_notitle():
    return render_template('sample_frontend/portfolio-5-notitle.html')


@sample_frontend.route('/event_single_left_sidebar')
def event_single_left_sidebar():
    return render_template('sample_frontend/event-single-left-sidebar.html')


@sample_frontend.route('/columns_grids')
def columns_grids():
    return render_template('sample_frontend/columns-grids.html')


@sample_frontend.route('/portfolio_3_nomargin_left_sidebar')
def portfolio_3_nomargin_left_sidebar():
    return render_template('sample_frontend/portfolio-3-nomargin-left-sidebar.html')


@sample_frontend.route('/slider_revolution_kenburns')
def slider_revolution_kenburns():
    return render_template('sample_frontend/slider-revolution-kenburns.html')


@sample_frontend.route('/portfolio_single_gallery_both_sidebar')
def portfolio_single_gallery_both_sidebar():
    return render_template('sample_frontend/portfolio-single-gallery-both-sidebar.html')


@sample_frontend.route('/portfolio_1_alt_both_sidebar')
def portfolio_1_alt_both_sidebar():
    return render_template('sample_frontend/portfolio-1-alt-both-sidebar.html')


@sample_frontend.route('/shop_single_left_sidebar')
def shop_single_left_sidebar():
    return render_template('sample_frontend/shop-single-left-sidebar.html')


@sample_frontend.route('/slider_revolution_html5_videos')
def slider_revolution_html5_videos():
    return render_template('sample_frontend/slider-revolution-html5-videos.html')


@sample_frontend.route('/static_embed_video')
def static_embed_video():
    return render_template('sample_frontend/static-embed-video.html')


@sample_frontend.route('/combination_filter_select')
def combination_filter_select():
    return render_template('sample_frontend/combination-filter-select.html')


@sample_frontend.route('/portfolio_3_both_sidebar')
def portfolio_3_both_sidebar():
    return render_template('sample_frontend/portfolio-3-both-sidebar.html')


@sample_frontend.route('/demo_agency')
def demo_agency():
    return render_template('sample_frontend/demo-agency.html')


@sample_frontend.route('/shop_2_left_sidebar')
def shop_2_left_sidebar():
    return render_template('sample_frontend/shop-2-left-sidebar.html')


@sample_frontend.route('/index_portfolio_3')
def index_portfolio_3():
    return render_template('sample_frontend/index-portfolio-3.html')


@sample_frontend.route('/portfolio_single_video')
def portfolio_single_video():
    return render_template('sample_frontend/portfolio-single-video.html')


@sample_frontend.route('/shop_3')
def shop_3():
    return render_template('sample_frontend/shop-3.html')


@sample_frontend.route('/portfolio_2_both_sidebar')
def portfolio_2_both_sidebar():
    return render_template('sample_frontend/portfolio-2-both-sidebar.html')


@sample_frontend.route('/portfolio_1_alt_left_sidebar')
def portfolio_1_alt_left_sidebar():
    return render_template('sample_frontend/portfolio-1-alt-left-sidebar.html')


@sample_frontend.route('/portfolio_1_full_alt_both_sidebar')
def portfolio_1_full_alt_both_sidebar():
    return render_template('sample_frontend/portfolio-1-full-alt-both-sidebar.html')


@sample_frontend.route('/index_parallax')
def index_parallax():
    return render_template('sample_frontend/index-parallax.html')


@sample_frontend.route('/social_icons')
def social_icons():
    return render_template('sample_frontend/social-icons.html')


@sample_frontend.route('/megamenu_with_dropdown')
def megamenu_with_dropdown():
    return render_template('sample_frontend/megamenu-with-dropdown.html')


@sample_frontend.route('/portfolio_5_title_overlay')
def portfolio_5_title_overlay():
    return render_template('sample_frontend/portfolio-5-title-overlay.html')


@sample_frontend.route('/portfolio_mixed_masonry')
def portfolio_mixed_masonry():
    return render_template('sample_frontend/portfolio-mixed-masonry.html')


@sample_frontend.route('/services_2')
def services_2():
    return render_template('sample_frontend/services-2.html')


@sample_frontend.route('/portfolio_notitle')
def portfolio_notitle():
    return render_template('sample_frontend/portfolio-notitle.html')


@sample_frontend.route('/portfolio_single_thumbs_full')
def portfolio_single_thumbs_full():
    return render_template('sample_frontend/portfolio-single-thumbs-full.html')


@sample_frontend.route('/page_title_parallax')
def page_title_parallax():
    return render_template('sample_frontend/page-title-parallax.html')


@sample_frontend.route('/team')
def team():
    return render_template('sample_frontend/team.html')


@sample_frontend.route('/side_panel_left_overlay')
def side_panel_left_overlay():
    return render_template('sample_frontend/side-panel-left-overlay.html')


@sample_frontend.route('/portfolio_5_masonry_right_sidebar')
def portfolio_5_masonry_right_sidebar():
    return render_template('sample_frontend/portfolio-5-masonry-right-sidebar.html')


@sample_frontend.route('/both_sidebar')
def both_sidebar():
    return render_template('sample_frontend/both-sidebar.html')


@sample_frontend.route('/index_restaurant')
def index_restaurant():
    return render_template('sample_frontend/index-restaurant.html')


@sample_frontend.route('/shop_category_parallax')
def shop_category_parallax():
    return render_template('sample_frontend/shop-category-parallax.html')


@sample_frontend.route('/menu_5')
def menu_5():
    return render_template('sample_frontend/menu-5.html')


@sample_frontend.route('/portfolio_single_video_fullwidth_left_sidebar')
def portfolio_single_video_fullwidth_left_sidebar():
    return render_template('sample_frontend/portfolio-single-video-fullwidth-left-sidebar.html')


@sample_frontend.route('/portfolio_2_masonry_both_sidebar')
def portfolio_2_masonry_both_sidebar():
    return render_template('sample_frontend/portfolio-2-masonry-both-sidebar.html')


@sample_frontend.route('/process_steps')
def process_steps():
    return render_template('sample_frontend/process-steps.html')


@sample_frontend.route('/menu_2')
def menu_2():
    return render_template('sample_frontend/menu-2.html')


@sample_frontend.route('/slider_cheermonk_5')
def slider_cheermonk_5():
    return render_template('sample_frontend/slider-cheermonk-5.html')


@sample_frontend.route('/footer_2')
def footer_2():
    return render_template('sample_frontend/footer-2.html')


@sample_frontend.route('/portfolio_5_nomargin')
def portfolio_5_nomargin():
    return render_template('sample_frontend/portfolio-5-nomargin.html')


@sample_frontend.route('/jobs_file')
def jobs_file():
    return render_template('sample_frontend/jobs-file.html')


@sample_frontend.route('/portfolio_3_right_sidebar')
def portfolio_3_right_sidebar():
    return render_template('sample_frontend/portfolio-3-right-sidebar.html')


@sample_frontend.route('/portfolio_masonry')
def portfolio_masonry():
    return render_template('sample_frontend/portfolio-masonry.html')


@sample_frontend.route('/blog_single_split_left_sidebar')
def blog_single_split_left_sidebar():
    return render_template('sample_frontend/blog-single-split-left-sidebar.html')


@sample_frontend.route('/faqs_4')
def faqs_4():
    return render_template('sample_frontend/faqs-4.html')


@sample_frontend.route('/portfolio_single_video_left_sidebar')
def portfolio_single_video_left_sidebar():
    return render_template('sample_frontend/portfolio-single-video-left-sidebar.html')


@sample_frontend.route('/shop_1_right_sidebar')
def shop_1_right_sidebar():
    return render_template('sample_frontend/shop-1-right-sidebar.html')


@sample_frontend.route('/blog_timeline_2')
def blog_timeline_2():
    return render_template('sample_frontend/blog-timeline-2.html')


@sample_frontend.route('/portfolio_single_video_right_sidebar')
def portfolio_single_video_right_sidebar():
    return render_template('sample_frontend/portfolio-single-video-right-sidebar.html')


@sample_frontend.route('/blog_small_alt_left_sidebar')
def blog_small_alt_left_sidebar():
    return render_template('sample_frontend/blog-small-alt-left-sidebar.html')


@sample_frontend.route('/portfolio_5_masonry_nomargin_right_sidebar')
def portfolio_5_masonry_nomargin_right_sidebar():
    return render_template('sample_frontend/portfolio-5-masonry-nomargin-right-sidebar.html')


@sample_frontend.route('/portfolio_3_masonry_title_overlay')
def portfolio_3_masonry_title_overlay():
    return render_template('sample_frontend/portfolio-3-masonry-title-overlay.html')


@sample_frontend.route('/portfolio_hash_filter')
def portfolio_hash_filter():
    return render_template('sample_frontend/portfolio-hash-filter.html')


@sample_frontend.route('/event_single_right_sidebar')
def event_single_right_sidebar():
    return render_template('sample_frontend/event-single-right-sidebar.html')


@sample_frontend.route('/google_map_functions')
def google_map_functions():
    return render_template('sample_frontend/google-map-functions.html')


@sample_frontend.route('/portfolio_infinity_scroll_2')
def portfolio_infinity_scroll_2():
    return render_template('sample_frontend/portfolio-infinity-scroll-2.html')


@sample_frontend.route('/portfolio_single_gallery_full_meta_right')
def portfolio_single_gallery_full_meta_right():
    return render_template('sample_frontend/portfolio-single-gallery-full-meta-right.html')


@sample_frontend.route('/portfolio_masonry_nomargin_left_sidebar')
def portfolio_masonry_nomargin_left_sidebar():
    return render_template('sample_frontend/portfolio-masonry-nomargin-left-sidebar.html')


@sample_frontend.route('/portfolio_single_full_meta_right')
def portfolio_single_full_meta_right():
    return render_template('sample_frontend/portfolio-single-full-meta-right.html')


@sample_frontend.route('/portfolio_2_masonry_nomargin_left_sidebar')
def portfolio_2_masonry_nomargin_left_sidebar():
    return render_template('sample_frontend/portfolio-2-masonry-nomargin-left-sidebar.html')


@sample_frontend.route('/menu_8')
def menu_8():
    return render_template('sample_frontend/menu-8.html')


@sample_frontend.route('/side_panel_left_push')
def side_panel_left_push():
    return render_template('sample_frontend/side-panel-left-push.html')


@sample_frontend.route('/navigation')
def navigation():
    return render_template('sample_frontend/navigation.html')


@sample_frontend.route('/portfolio_6_fullwidth')
def portfolio_6_fullwidth():
    return render_template('sample_frontend/portfolio-6-fullwidth.html')


@sample_frontend.route('/contact_6')
def contact_6():
    return render_template('sample_frontend/contact-6.html')


@sample_frontend.route('/portfolio_2_notitle_right_sidebar')
def portfolio_2_notitle_right_sidebar():
    return render_template('sample_frontend/portfolio-2-notitle-right-sidebar.html')


@sample_frontend.route('/portfolio_notitle_right_sidebar')
def portfolio_notitle_right_sidebar():
    return render_template('sample_frontend/portfolio-notitle-right-sidebar.html')


@sample_frontend.route('/landing_3')
def landing_3():
    return render_template('sample_frontend/landing-3.html')


@sample_frontend.route('/blog')
def blog():
    return render_template('sample_frontend/blog.html')


@sample_frontend.route('/shop_single')
def shop_single():
    return render_template('sample_frontend/shop-single.html')


@sample_frontend.route('/portfolio_single_thumbs_fullwidth_both_sidebar')
def portfolio_single_thumbs_fullwidth_both_sidebar():
    return render_template('sample_frontend/portfolio-single-thumbs-fullwidth-both-sidebar.html')


@sample_frontend.route('/portfolio_5_left_sidebar')
def portfolio_5_left_sidebar():
    return render_template('sample_frontend/portfolio-5-left-sidebar.html')


@sample_frontend.route('/slider_cheermonk_autoplay')
def slider_cheermonk_autoplay():
    return render_template('sample_frontend/slider-cheermonk-autoplay.html')


@sample_frontend.route('/services_3')
def services_3():
    return render_template('sample_frontend/services-3.html')


@sample_frontend.route('/services')
def services():
    return render_template('sample_frontend/services.html')


@sample_frontend.route('/menu_3')
def menu_3():
    return render_template('sample_frontend/menu-3.html')


@sample_frontend.route('/portfolio_ajax')
def portfolio_ajax():
    return render_template('sample_frontend/portfolio-ajax.html')


@sample_frontend.route('/page_title_dark')
def page_title_dark():
    return render_template('sample_frontend/page-title-dark.html')


@sample_frontend.route('/blog_small_alt_full_width')
def blog_small_alt_full_width():
    return render_template('sample_frontend/blog-small-alt-full-width.html')


@sample_frontend.route('/portfolio_5_masonry')
def portfolio_5_masonry():
    return render_template('sample_frontend/portfolio-5-masonry.html')


@sample_frontend.route('/portfolio_title_overlay')
def portfolio_title_overlay():
    return render_template('sample_frontend/portfolio-title-overlay.html')


@sample_frontend.route('/demo_medical')
def demo_medical():
    return render_template('sample_frontend/demo-medical.html')


@sample_frontend.route('/portfolio_1_full_alt_right_sidebar')
def portfolio_1_full_alt_right_sidebar():
    return render_template('sample_frontend/portfolio-1-full-alt-right-sidebar.html')


@sample_frontend.route('/blog_timeline_right_sidebar')
def blog_timeline_right_sidebar():
    return render_template('sample_frontend/blog-timeline-right-sidebar.html')


@sample_frontend.route('/blog_small_alt_both_sidebar')
def blog_small_alt_both_sidebar():
    return render_template('sample_frontend/blog-small-alt-both-sidebar.html')


@sample_frontend.route('/modal_popovers')
def modal_popovers():
    return render_template('sample_frontend/modal-popovers.html')


@sample_frontend.route('/404_3')
def 404_3():
    return render_template('sample_frontend/404-3.html')


@sample_frontend.route('/faqs')
def faqs():
    return render_template('sample_frontend/faqs.html')


@sample_frontend.route('/portfolio_1_alt')
def portfolio_1_alt():
    return render_template('sample_frontend/portfolio-1-alt.html')


@sample_frontend.route('/portfolio_single_video_full_meta_right')
def portfolio_single_video_full_meta_right():
    return render_template('sample_frontend/portfolio-single-video-full-meta-right.html')


@sample_frontend.route('/header_side_right_open')
def header_side_right_open():
    return render_template('sample_frontend/header-side-right-open.html')


@sample_frontend.route('/portfolio_single_right_sidebar')
def portfolio_single_right_sidebar():
    return render_template('sample_frontend/portfolio-single-right-sidebar.html')


@sample_frontend.route('/slider_revolution')
def slider_revolution():
    return render_template('sample_frontend/slider-revolution.html')


@sample_frontend.route('/tables')
def tables():
    return render_template('sample_frontend/tables.html')


@sample_frontend.route('/blog_masonry_2_left_sidebar')
def blog_masonry_2_left_sidebar():
    return render_template('sample_frontend/blog-masonry-2-left-sidebar.html')


@sample_frontend.route('/portfolio_single')
def portfolio_single():
    return render_template('sample_frontend/portfolio-single.html')


@sample_frontend.route('/menu_9')
def menu_9():
    return render_template('sample_frontend/menu-9.html')


@sample_frontend.route('/carousel')
def carousel():
    return render_template('sample_frontend/carousel.html')


@sample_frontend.route('/portfolio_2_masonry_nomargin_right_sidebar')
def portfolio_2_masonry_nomargin_right_sidebar():
    return render_template('sample_frontend/portfolio-2-masonry-nomargin-right-sidebar.html')


@sample_frontend.route('/tabs')
def tabs():
    return render_template('sample_frontend/tabs.html')


@sample_frontend.route('/static_html5_video')
def static_html5_video():
    return render_template('sample_frontend/static-html5-video.html')


@sample_frontend.route('/left_sidebar')
def left_sidebar():
    return render_template('sample_frontend/left-sidebar.html')


@sample_frontend.route('/portfolio_single_thumbs_right_sidebar')
def portfolio_single_thumbs_right_sidebar():
    return render_template('sample_frontend/portfolio-single-thumbs-right-sidebar.html')


@sample_frontend.route('/login_register')
def login_register():
    return render_template('sample_frontend/login-register.html')


@sample_frontend.route('/checkout')
def checkout():
    return render_template('sample_frontend/checkout.html')


@sample_frontend.route('/blog_masonry_3_right_sidebar')
def blog_masonry_3_right_sidebar():
    return render_template('sample_frontend/blog-masonry-3-right-sidebar.html')


@sample_frontend.route('/shop_3_right_sidebar')
def shop_3_right_sidebar():
    return render_template('sample_frontend/shop-3-right-sidebar.html')


@sample_frontend.route('/')
def index():
    return render_template('sample_frontend/index.html')


@sample_frontend.route('/coming_soon')
def coming_soon():
    return render_template('sample_frontend/coming-soon.html')


@sample_frontend.route('/jobs')
def jobs():
    return render_template('sample_frontend/jobs.html')


@sample_frontend.route('/portfolio_2_notitle')
def portfolio_2_notitle():
    return render_template('sample_frontend/portfolio-2-notitle.html')


@sample_frontend.route('/search_in_header')
def search_in_header():
    return render_template('sample_frontend/search-in-header.html')


@sample_frontend.route('/combination_filter')
def combination_filter():
    return render_template('sample_frontend/combination-filter.html')


@sample_frontend.route('/portfolio_nomargin')
def portfolio_nomargin():
    return render_template('sample_frontend/portfolio-nomargin.html')


@sample_frontend.route('/portfolio_3_nomargin_right_sidebar')
def portfolio_3_nomargin_right_sidebar():
    return render_template('sample_frontend/portfolio-3-nomargin-right-sidebar.html')


@sample_frontend.route('/blog_masonry_page_2')
def blog_masonry_page_2():
    return render_template('sample_frontend/blog-masonry-page-2.html')


@sample_frontend.route('/portfolio_1_full')
def portfolio_1_full():
    return render_template('sample_frontend/portfolio-1-full.html')


@sample_frontend.route('/portfolio_3_notitle_both_sidebar')
def portfolio_3_notitle_both_sidebar():
    return render_template('sample_frontend/portfolio-3-notitle-both-sidebar.html')


@sample_frontend.route('/testimonials_twitter')
def testimonials_twitter():
    return render_template('sample_frontend/testimonials-twitter.html')


@sample_frontend.route('/captcha_footer_form')
def captcha_footer_form():
    return render_template('sample_frontend/captcha-footer-form.html')


@sample_frontend.route('/responsive')
def responsive():
    return render_template('sample_frontend/responsive.html')


@sample_frontend.route('/vertical_nav')
def vertical_nav():
    return render_template('sample_frontend/vertical-nav.html')


@sample_frontend.route('/blog_single_split_both_sidebar')
def blog_single_split_both_sidebar():
    return render_template('sample_frontend/blog-single-split-both-sidebar.html')


@sample_frontend.route('/featured_boxes')
def featured_boxes():
    return render_template('sample_frontend/featured-boxes.html')


@sample_frontend.route('/index_corporate_4')
def index_corporate_4():
    return render_template('sample_frontend/index-corporate-4.html')


@sample_frontend.route('/portfolio_2_masonry_left_sidebar')
def portfolio_2_masonry_left_sidebar():
    return render_template('sample_frontend/portfolio-2-masonry-left-sidebar.html')


@sample_frontend.route('/slider_cheermonk_pagination')
def slider_cheermonk_pagination():
    return render_template('sample_frontend/slider-cheermonk-pagination.html')


@sample_frontend.route('/index_fullscreen_video')
def index_fullscreen_video():
    return render_template('sample_frontend/index-fullscreen-video.html')


@sample_frontend.route('/portfolio_single_thumbs_full_meta_right')
def portfolio_single_thumbs_full_meta_right():
    return render_template('sample_frontend/portfolio-single-thumbs-full-meta-right.html')


@sample_frontend.route('/portfolio_single_gallery_fullwidth_left_sidebar')
def portfolio_single_gallery_fullwidth_left_sidebar():
    return render_template('sample_frontend/portfolio-single-gallery-fullwidth-left-sidebar.html')


@sample_frontend.route('/portfolio_hash_filter_darkrainbow')
def portfolio_hash_filter_darkrainbow():
    return render_template('sample_frontend/portfolio-hash-filter-darkrainbow.html')


@sample_frontend.route('/page_title_parallax_header')
def page_title_parallax_header():
    return render_template('sample_frontend/page-title-parallax-header.html')


@sample_frontend.route('/side_panel')
def side_panel():
    return render_template('sample_frontend/side-panel.html')


@sample_frontend.route('/portfolio_5_nomargin_right_sidebar')
def portfolio_5_nomargin_right_sidebar():
    return render_template('sample_frontend/portfolio-5-nomargin-right-sidebar.html')


@sample_frontend.route('/portfolio_parallax')
def portfolio_parallax():
    return render_template('sample_frontend/portfolio-parallax.html')


@sample_frontend.route('/header_floating')
def header_floating():
    return render_template('sample_frontend/header-floating.html')


@sample_frontend.route('/shop_single_both_sidebar')
def shop_single_both_sidebar():
    return render_template('sample_frontend/shop-single-both-sidebar.html')


@sample_frontend.route('/search')
def search():
    return render_template('sample_frontend/search.html')


@sample_frontend.route('/portfolio_single_thumbs_both_sidebar')
def portfolio_single_thumbs_both_sidebar():
    return render_template('sample_frontend/portfolio-single-thumbs-both-sidebar.html')


@sample_frontend.route('/portfolio_2_nomargin_left_sidebar')
def portfolio_2_nomargin_left_sidebar():
    return render_template('sample_frontend/portfolio-2-nomargin-left-sidebar.html')


@sample_frontend.route('/portfolio_masonry_nomargin_right_sidebar')
def portfolio_masonry_nomargin_right_sidebar():
    return render_template('sample_frontend/portfolio-masonry-nomargin-right-sidebar.html')


@sample_frontend.route('/blog_full_width')
def blog_full_width():
    return render_template('sample_frontend/blog-full-width.html')


@sample_frontend.route('/index_corporate')
def index_corporate():
    return render_template('sample_frontend/index-corporate.html')


@sample_frontend.route('/static_image')
def static_image():
    return render_template('sample_frontend/static-image.html')


@sample_frontend.route('/portfolio_single_video_fullwidth_right_sidebar')
def portfolio_single_video_fullwidth_right_sidebar():
    return render_template('sample_frontend/portfolio-single-video-fullwidth-right-sidebar.html')


@sample_frontend.route('/portfolio_pagination')
def portfolio_pagination():
    return render_template('sample_frontend/portfolio-pagination.html')


@sample_frontend.route('/gallery')
def gallery():
    return render_template('sample_frontend/gallery.html')


@sample_frontend.route('/contact_3')
def contact_3():
    return render_template('sample_frontend/contact-3.html')


@sample_frontend.route('/portfolio_5_fullwidth')
def portfolio_5_fullwidth():
    return render_template('sample_frontend/portfolio-5-fullwidth.html')


@sample_frontend.route('/page')
def page():
    return render_template('sample_frontend/page.html')


@sample_frontend.route('/footer_7')
def footer_7():
    return render_template('sample_frontend/footer-7.html')


@sample_frontend.route('/slider_flex')
def slider_flex():
    return render_template('sample_frontend/slider-flex.html')


@sample_frontend.route('/page_title_nobg')
def page_title_nobg():
    return render_template('sample_frontend/page-title-nobg.html')


@sample_frontend.route('/portfolio_single_video_fullwidth')
def portfolio_single_video_fullwidth():
    return render_template('sample_frontend/portfolio-single-video-fullwidth.html')


@sample_frontend.route('/portfolio_5_masonry_left_sidebar')
def portfolio_5_masonry_left_sidebar():
    return render_template('sample_frontend/portfolio-5-masonry-left-sidebar.html')


@sample_frontend.route('/header_light')
def header_light():
    return render_template('sample_frontend/header-light.html')


@sample_frontend.route('/side_panel_light')
def side_panel_light():
    return render_template('sample_frontend/side-panel-light.html')


@sample_frontend.route('/portfolio_6_masonry_nomargin')
def portfolio_6_masonry_nomargin():
    return render_template('sample_frontend/portfolio-6-masonry-nomargin.html')


@sample_frontend.route('/events_list_fullwidth')
def events_list_fullwidth():
    return render_template('sample_frontend/events-list-fullwidth.html')


@sample_frontend.route('/portfolio_1_full_alt_left_sidebar')
def portfolio_1_full_alt_left_sidebar():
    return render_template('sample_frontend/portfolio-1-full-alt-left-sidebar.html')


@sample_frontend.route('/animations')
def animations():
    return render_template('sample_frontend/animations.html')


@sample_frontend.route('/slider_flex_thumbs')
def slider_flex_thumbs():
    return render_template('sample_frontend/slider-flex-thumbs.html')


@sample_frontend.route('/full_width_wide')
def full_width_wide():
    return render_template('sample_frontend/full-width-wide.html')


@sample_frontend.route('/slider_cheermonk_4')
def slider_cheermonk_4():
    return render_template('sample_frontend/slider-cheermonk-4.html')


@sample_frontend.route('/portfolio_infinity_scroll_3')
def portfolio_infinity_scroll_3():
    return render_template('sample_frontend/portfolio-infinity-scroll-3.html')


@sample_frontend.route('/blog_timeline')
def blog_timeline():
    return render_template('sample_frontend/blog-timeline.html')


@sample_frontend.route('/portfolio_6_notitle')
def portfolio_6_notitle():
    return render_template('sample_frontend/portfolio-6-notitle.html')


@sample_frontend.route('/clients')
def clients():
    return render_template('sample_frontend/clients.html')


@sample_frontend.route('/portfolio_6_nomargin')
def portfolio_6_nomargin():
    return render_template('sample_frontend/portfolio-6-nomargin.html')


@sample_frontend.route('/index_shop_2')
def index_shop_2():
    return render_template('sample_frontend/index-shop-2.html')


@sample_frontend.route('/portfolio')
def portfolio():
    return render_template('sample_frontend/portfolio.html')


@sample_frontend.route('/both_right_sidebar')
def both_right_sidebar():
    return render_template('sample_frontend/both-right-sidebar.html')


@sample_frontend.route('/portfolio_3_masonry_nomargin_both_sidebar')
def portfolio_3_masonry_nomargin_both_sidebar():
    return render_template('sample_frontend/portfolio-3-masonry-nomargin-both-sidebar.html')


@sample_frontend.route('/page_title')
def page_title():
    return render_template('sample_frontend/page-title.html')


@sample_frontend.route('/coming_soon_3')
def coming_soon_3():
    return render_template('sample_frontend/coming-soon-3.html')


@sample_frontend.route('/both_left_sidebar')
def both_left_sidebar():
    return render_template('sample_frontend/both-left-sidebar.html')


@sample_frontend.route('/conditional_form')
def conditional_form():
    return render_template('sample_frontend/conditional-form.html')


@sample_frontend.route('/about_me')
def about_me():
    return render_template('sample_frontend/about-me.html')


@sample_frontend.route('/slider_cheermonk_video_event')
def slider_cheermonk_video_event():
    return render_template('sample_frontend/slider-cheermonk-video-event.html')


@sample_frontend.route('/blog_small_left_sidebar')
def blog_small_left_sidebar():
    return render_template('sample_frontend/blog-small-left-sidebar.html')


@sample_frontend.route('/sticky_footer')
def sticky_footer():
    return render_template('sample_frontend/sticky-footer.html')


@sample_frontend.route('/index_portfolio_2')
def index_portfolio_2():
    return render_template('sample_frontend/index-portfolio-2.html')


@sample_frontend.route('/contact_4')
def contact_4():
    return render_template('sample_frontend/contact-4.html')


@sample_frontend.route('/portfolio_1_left_sidebar')
def portfolio_1_left_sidebar():
    return render_template('sample_frontend/portfolio-1-left-sidebar.html')


@sample_frontend.route('/login_1')
def login_1():
    return render_template('sample_frontend/login-1.html')


@sample_frontend.route('/portfolio_3_left_sidebar')
def portfolio_3_left_sidebar():
    return render_template('sample_frontend/portfolio-3-left-sidebar.html')


@sample_frontend.route('/portfolio_5_right_sidebar')
def portfolio_5_right_sidebar():
    return render_template('sample_frontend/portfolio-5-right-sidebar.html')


@sample_frontend.route('/portfolio_3_fullwidth_notitle')
def portfolio_3_fullwidth_notitle():
    return render_template('sample_frontend/portfolio-3-fullwidth-notitle.html')


@sample_frontend.route('/events_calendar')
def events_calendar():
    return render_template('sample_frontend/events-calendar.html')


@sample_frontend.route('/portfolio_ajax_in_modal')
def portfolio_ajax_in_modal():
    return render_template('sample_frontend/portfolio-ajax-in-modal.html')


@sample_frontend.route('/shop')
def shop():
    return render_template('sample_frontend/shop.html')


@sample_frontend.route('/portfolio_single_gallery')
def portfolio_single_gallery():
    return render_template('sample_frontend/portfolio-single-gallery.html')


@sample_frontend.route('/portfolio_1_full_left_sidebar')
def portfolio_1_full_left_sidebar():
    return render_template('sample_frontend/portfolio-1-full-left-sidebar.html')


@sample_frontend.route('/demo_media_agency')
def demo_media_agency():
    return render_template('sample_frontend/demo-media-agency.html')


@sample_frontend.route('/thumbnails_slider')
def thumbnails_slider():
    return render_template('sample_frontend/thumbnails-slider.html')


@sample_frontend.route('/sections')
def sections():
    return render_template('sample_frontend/sections.html')


@sample_frontend.route('/portfolio_5_notitle_left_sidebar')
def portfolio_5_notitle_left_sidebar():
    return render_template('sample_frontend/portfolio-5-notitle-left-sidebar.html')


@sample_frontend.route('/menu_7')
def menu_7():
    return render_template('sample_frontend/menu-7.html')


@sample_frontend.route('/portfolio_1_right_sidebar')
def portfolio_1_right_sidebar():
    return render_template('sample_frontend/portfolio-1-right-sidebar.html')


@sample_frontend.route('/about_2')
def about_2():
    return render_template('sample_frontend/about-2.html')


@sample_frontend.route('/portfolio_single_thumbs_fullwidth_left_sidebar')
def portfolio_single_thumbs_fullwidth_left_sidebar():
    return render_template('sample_frontend/portfolio-single-thumbs-fullwidth-left-sidebar.html')


@sample_frontend.route('/blog_single_small_left_sidebar')
def blog_single_small_left_sidebar():
    return render_template('sample_frontend/blog-single-small-left-sidebar.html')


@sample_frontend.route('/page_title_video')
def page_title_video():
    return render_template('sample_frontend/page-title-video.html')


@sample_frontend.route('/index_onepage')
def index_onepage():
    return render_template('sample_frontend/index-onepage.html')


@sample_frontend.route('/portfolio_5_fullwidth_notitle')
def portfolio_5_fullwidth_notitle():
    return render_template('sample_frontend/portfolio-5-fullwidth-notitle.html')


@sample_frontend.route('/portfolio_5_notitle_right_sidebar')
def portfolio_5_notitle_right_sidebar():
    return render_template('sample_frontend/portfolio-5-notitle-right-sidebar.html')


@sample_frontend.route('/about')
def about():
    return render_template('sample_frontend/about.html')


@sample_frontend.route('/shop_single_right_sidebar')
def shop_single_right_sidebar():
    return render_template('sample_frontend/shop-single-right-sidebar.html')


@sample_frontend.route('/index_video_sound_event')
def index_video_sound_event():
    return render_template('sample_frontend/index-video-sound-event.html')


@sample_frontend.route('/lists_panels')
def lists_panels():
    return render_template('sample_frontend/lists-panels.html')


@sample_frontend.route('/portfolio_single_gallery_fullwidth_both_sidebar')
def portfolio_single_gallery_fullwidth_both_sidebar():
    return render_template('sample_frontend/portfolio-single-gallery-fullwidth-both-sidebar.html')


@sample_frontend.route('/blog_masonry')
def blog_masonry():
    return render_template('sample_frontend/blog-masonry.html')


@sample_frontend.route('/portfolio_both_sidebar')
def portfolio_both_sidebar():
    return render_template('sample_frontend/portfolio-both-sidebar.html')


@sample_frontend.route('/portfolio_3_masonry_nomargin_left_sidebar')
def portfolio_3_masonry_nomargin_left_sidebar():
    return render_template('sample_frontend/portfolio-3-masonry-nomargin-left-sidebar.html')


@sample_frontend.route('/portfolio_3_notitle')
def portfolio_3_notitle():
    return render_template('sample_frontend/portfolio-3-notitle.html')


@sample_frontend.route('/index_events')
def index_events():
    return render_template('sample_frontend/index-events.html')


@sample_frontend.route('/portfolio_2_masonry_nomargin_both_sidebar')
def portfolio_2_masonry_nomargin_both_sidebar():
    return render_template('sample_frontend/portfolio-2-masonry-nomargin-both-sidebar.html')


@sample_frontend.route('/portfolio_3_notitle_left_sidebar')
def portfolio_3_notitle_left_sidebar():
    return render_template('sample_frontend/portfolio-3-notitle-left-sidebar.html')


@sample_frontend.route('/side_navigation')
def side_navigation():
    return render_template('sample_frontend/side-navigation.html')


@sample_frontend.route('/portfolio_2')
def portfolio_2():
    return render_template('sample_frontend/portfolio-2.html')


@sample_frontend.route('/modal_onload')
def modal_onload():
    return render_template('sample_frontend/modal-onload.html')


@sample_frontend.route('/side_panel_right_overlay')
def side_panel_right_overlay():
    return render_template('sample_frontend/side-panel-right-overlay.html')


@sample_frontend.route('/portfolio_6_masonry_title_overlay')
def portfolio_6_masonry_title_overlay():
    return render_template('sample_frontend/portfolio-6-masonry-title-overlay.html')


@sample_frontend.route('/portfolio_2_left_sidebar')
def portfolio_2_left_sidebar():
    return render_template('sample_frontend/portfolio-2-left-sidebar.html')


@sample_frontend.route('/blog_masonry_3_left_sidebar')
def blog_masonry_3_left_sidebar():
    return render_template('sample_frontend/blog-masonry-3-left-sidebar.html')


@sample_frontend.route('/buttons')
def buttons():
    return render_template('sample_frontend/buttons.html')


@sample_frontend.route('/slider_cheermonk')
def slider_cheermonk():
    return render_template('sample_frontend/slider-cheermonk.html')


@sample_frontend.route('/portfolio_single_video_both_sidebar')
def portfolio_single_video_both_sidebar():
    return render_template('sample_frontend/portfolio-single-video-both-sidebar.html')


@sample_frontend.route('/header_semi_transparent')
def header_semi_transparent():
    return render_template('sample_frontend/header-semi-transparent.html')


@sample_frontend.route('/slider_cheermonk_3')
def slider_cheermonk_3():
    return render_template('sample_frontend/slider-cheermonk-3.html')


@sample_frontend.route('/shop_1')
def shop_1():
    return render_template('sample_frontend/shop-1.html')


@sample_frontend.route('/maps')
def maps():
    return render_template('sample_frontend/maps.html')


@sample_frontend.route('/one_page_scroll')
def one_page_scroll():
    return render_template('sample_frontend/one-page-scroll.html')


@sample_frontend.route('/portfolio_5_masonry_nomargin_left_sidebar')
def portfolio_5_masonry_nomargin_left_sidebar():
    return render_template('sample_frontend/portfolio-5-masonry-nomargin-left-sidebar.html')


@sample_frontend.route('/labels_badges')
def labels_badges():
    return render_template('sample_frontend/labels-badges.html')


@sample_frontend.route('/portfolio_single_thumbs_right')
def portfolio_single_thumbs_right():
    return render_template('sample_frontend/portfolio-single-thumbs-right.html')


@sample_frontend.route('/header_side_right_open_push')
def header_side_right_open_push():
    return render_template('sample_frontend/header-side-right-open-push.html')


@sample_frontend.route('/gallery_filter')
def gallery_filter():
    return render_template('sample_frontend/gallery-filter.html')


@sample_frontend.route('/headings_dropcaps')
def headings_dropcaps():
    return render_template('sample_frontend/headings-dropcaps.html')


@sample_frontend.route('/login_register_3')
def login_register_3():
    return render_template('sample_frontend/login-register-3.html')


@sample_frontend.route('/portfolio_single_gallery_right_sidebar')
def portfolio_single_gallery_right_sidebar():
    return render_template('sample_frontend/portfolio-single-gallery-right-sidebar.html')


@sample_frontend.route('/slider_nivo')
def slider_nivo():
    return render_template('sample_frontend/slider-nivo.html')


@sample_frontend.route('/modal_onload_common_height')
def modal_onload_common_height():
    return render_template('sample_frontend/modal-onload-common-height.html')


@sample_frontend.route('/blog_masonry_3_full')
def blog_masonry_3_full():
    return render_template('sample_frontend/blog-masonry-3-full.html')


@sample_frontend.route('/index_fullscreen_slider')
def index_fullscreen_slider():
    return render_template('sample_frontend/index-fullscreen-slider.html')


@sample_frontend.route('/page_submenu')
def page_submenu():
    return render_template('sample_frontend/page-submenu.html')


@sample_frontend.route('/blog_single_small_full')
def blog_single_small_full():
    return render_template('sample_frontend/blog-single-small-full.html')


@sample_frontend.route('/portfolio_single_thumbs')
def portfolio_single_thumbs():
    return render_template('sample_frontend/portfolio-single-thumbs.html')


@sample_frontend.route('/index_corporate_3')
def index_corporate_3():
    return render_template('sample_frontend/index-corporate-3.html')


@sample_frontend.route('/portfolio_single_gallery_left_sidebar')
def portfolio_single_gallery_left_sidebar():
    return render_template('sample_frontend/portfolio-single-gallery-left-sidebar.html')


@sample_frontend.route('/blog_grid_3')
def blog_grid_3():
    return render_template('sample_frontend/blog-grid-3.html')


@sample_frontend.route('/blog_masonry_2_right_sidebar')
def blog_masonry_2_right_sidebar():
    return render_template('sample_frontend/blog-masonry-2-right-sidebar.html')


@sample_frontend.route('/portfolio_3_masonry_nomargin')
def portfolio_3_masonry_nomargin():
    return render_template('sample_frontend/portfolio-3-masonry-nomargin.html')


@sample_frontend.route('/portfolio_2_nomargin_right_sidebar')
def portfolio_2_nomargin_right_sidebar():
    return render_template('sample_frontend/portfolio-2-nomargin-right-sidebar.html')


@sample_frontend.route('/event_single_full_width_video')
def event_single_full_width_video():
    return render_template('sample_frontend/event-single-full-width-video.html')


@sample_frontend.route('/demo_travel')
def demo_travel():
    return render_template('sample_frontend/demo-travel.html')


@sample_frontend.route('/page_title_gmap')
def page_title_gmap():
    return render_template('sample_frontend/page-title-gmap.html')


@sample_frontend.route('/portfolio_single_fullwidth')
def portfolio_single_fullwidth():
    return render_template('sample_frontend/portfolio-single-fullwidth.html')


@sample_frontend.route('/portfolio_single_gallery_right')
def portfolio_single_gallery_right():
    return render_template('sample_frontend/portfolio-single-gallery-right.html')


@sample_frontend.route('/contact_file')
def contact_file():
    return render_template('sample_frontend/contact-file.html')


@sample_frontend.route('/quotes_blockquotes')
def quotes_blockquotes():
    return render_template('sample_frontend/quotes-blockquotes.html')


@sample_frontend.route('/event_single')
def event_single():
    return render_template('sample_frontend/event-single.html')


@sample_frontend.route('/contact')
def contact():
    return render_template('sample_frontend/contact.html')


@sample_frontend.route('/shop_3_left_sidebar')
def shop_3_left_sidebar():
    return render_template('sample_frontend/shop-3-left-sidebar.html')


@sample_frontend.route('/promo_boxes')
def promo_boxes():
    return render_template('sample_frontend/promo-boxes.html')


@sample_frontend.route('/404')
def 404():
    return render_template('sample_frontend/404.html')


@sample_frontend.route('/portfolio_3_masonry_nomargin_right_sidebar')
def portfolio_3_masonry_nomargin_right_sidebar():
    return render_template('sample_frontend/portfolio-3-masonry-nomargin-right-sidebar.html')


@sample_frontend.route('/landing_5')
def landing_5():
    return render_template('sample_frontend/landing-5.html')


@sample_frontend.route('/portfolio_3_title_overlay')
def portfolio_3_title_overlay():
    return render_template('sample_frontend/portfolio-3-title-overlay.html')


@sample_frontend.route('/include_ajax_portfolio_single_image')
def include_ajax_portfolio_single_image():
    return render_template('sample_frontend/include/ajax/portfolio-single-image.html')


@sample_frontend.route('/include_ajax_shop_item')
def include_ajax_shop_item():
    return render_template('sample_frontend/include/ajax/shop-item.html')


@sample_frontend.route('/include_ajax_portfolio_single_video')
def include_ajax_portfolio_single_video():
    return render_template('sample_frontend/include/ajax/portfolio-single-video.html')


@sample_frontend.route('/include_ajax_portfolio_single_gallery')
def include_ajax_portfolio_single_gallery():
    return render_template('sample_frontend/include/ajax/portfolio-single-gallery.html')


@sample_frontend.route('/include_ajax_portfolio_single_thumbs')
def include_ajax_portfolio_single_thumbs():
    return render_template('sample_frontend/include/ajax/portfolio-single-thumbs.html')


@sample_frontend.route('/one_page_op_parallax_dark_image_full')
def one_page_op_parallax_dark_image_full():
    return render_template('sample_frontend/one-page/op-parallax-dark-image-full.html')


@sample_frontend.route('/one_page_op_portfolio')
def one_page_op_portfolio():
    return render_template('sample_frontend/one-page/op-portfolio.html')


@sample_frontend.route('/one_page_op_register')
def one_page_op_register():
    return render_template('sample_frontend/one-page/op-register.html')


@sample_frontend.route('/one_page_op_video_event')
def one_page_op_video_event():
    return render_template('sample_frontend/one-page/op-video-event.html')


@sample_frontend.route('/one_page_index_dark')
def one_page_index_dark():
    return render_template('sample_frontend/one-page/index-dark.html')


@sample_frontend.route('/one_page_op_owl_slider')
def one_page_op_owl_slider():
    return render_template('sample_frontend/one-page/op-owl-slider.html')


@sample_frontend.route('/one_page_op_parallax_dark_image_fullwidth')
def one_page_op_parallax_dark_image_fullwidth():
    return render_template('sample_frontend/one-page/op-parallax-dark-image-fullwidth.html')


@sample_frontend.route('/one_page_op_side_header')
def one_page_op_side_header():
    return render_template('sample_frontend/one-page/op-side-header.html')


@sample_frontend.route('/one_page_op_section_2')
def one_page_op_section_2():
    return render_template('sample_frontend/one-page/op-section-2.html')


@sample_frontend.route('/one_page_op_tr_image_dark')
def one_page_op_tr_image_dark():
    return render_template('sample_frontend/one-page/op-tr-image-dark.html')


@sample_frontend.route('/one_page_op_event')
def one_page_op_event():
    return render_template('sample_frontend/one-page/op-event.html')


@sample_frontend.route('/one_page_op_html5_video_dark')
def one_page_op_html5_video_dark():
    return render_template('sample_frontend/one-page/op-html5-video-dark.html')


@sample_frontend.route('/one_page_op_video_grid')
def one_page_op_video_grid():
    return render_template('sample_frontend/one-page/op-video-grid.html')


@sample_frontend.route('/one_page_op_revolution_fullscreen')
def one_page_op_revolution_fullscreen():
    return render_template('sample_frontend/one-page/op-revolution-fullscreen.html')


@sample_frontend.route('/one_page_op_parallax_light_image_full')
def one_page_op_parallax_light_image_full():
    return render_template('sample_frontend/one-page/op-parallax-light-image-full.html')


@sample_frontend.route('/one_page_op_portfolio_side_header')
def one_page_op_portfolio_side_header():
    return render_template('sample_frontend/one-page/op-portfolio-side-header.html')


@sample_frontend.route('/one_page_op_tr_image_light')
def one_page_op_tr_image_light():
    return render_template('sample_frontend/one-page/op-tr-image-light.html')


@sample_frontend.route('/one_page_op_parallax_light_image_fullwidth')
def one_page_op_parallax_light_image_fullwidth():
    return render_template('sample_frontend/one-page/op-parallax-light-image-fullwidth.html')


@sample_frontend.route('/one_page_op_browser')
def one_page_op_browser():
    return render_template('sample_frontend/one-page/op-browser.html')


@sample_frontend.route('/one_page_op_counter')
def one_page_op_counter():
    return render_template('sample_frontend/one-page/op-counter.html')


@sample_frontend.route('/one_page_op_dots')
def one_page_op_dots():
    return render_template('sample_frontend/one-page/op-dots.html')


@sample_frontend.route('/one_page_op_section')
def one_page_op_section():
    return render_template('sample_frontend/one-page/op-section.html')


@sample_frontend.route('/one_page_op_device')
def one_page_op_device():
    return render_template('sample_frontend/one-page/op-device.html')


@sample_frontend.route('/one_page_op_owl_slider_video')
def one_page_op_owl_slider_video():
    return render_template('sample_frontend/one-page/op-owl-slider-video.html')


@sample_frontend.route('/one_page_op_register_testimonials')
def one_page_op_register_testimonials():
    return render_template('sample_frontend/one-page/op-register-testimonials.html')


@sample_frontend.route('/one_page_op_video_grid_2')
def one_page_op_video_grid_2():
    return render_template('sample_frontend/one-page/op-video-grid-2.html')


@sample_frontend.route('/one_page_op_tr_blank')
def one_page_op_tr_blank():
    return render_template('sample_frontend/one-page/op-tr-blank.html')


@sample_frontend.route('/one_page_index')
def one_page_index():
    return render_template('sample_frontend/one-page/index.html')


@sample_frontend.route('/one_page_op_cheermonk_slider')
def one_page_op_cheermonk_slider():
    return render_template('sample_frontend/one-page/op-cheermonk-slider.html')


@sample_frontend.route('/one_page_op_register_2')
def one_page_op_register_2():
    return render_template('sample_frontend/one-page/op-register-2.html')


@sample_frontend.route('/one_page_op_chart')
def one_page_op_chart():
    return render_template('sample_frontend/one-page/op-chart.html')


@sample_frontend.route('/one_page_op_lightbox_video')
def one_page_op_lightbox_video():
    return render_template('sample_frontend/one-page/op-lightbox-video.html')


@sample_frontend.route('/one_page_op_image_grid_video_lightbox')
def one_page_op_image_grid_video_lightbox():
    return render_template('sample_frontend/one-page/op-image-grid-video-lightbox.html')


@sample_frontend.route('/one_page_op_tr_blank_dark')
def one_page_op_tr_blank_dark():
    return render_template('sample_frontend/one-page/op-tr-blank-dark.html')


@sample_frontend.route('/one_page_op_subscription')
def one_page_op_subscription():
    return render_template('sample_frontend/one-page/op-subscription.html')


@sample_frontend.route('/one_page_op_counter_2')
def one_page_op_counter_2():
    return render_template('sample_frontend/one-page/op-counter-2.html')


@sample_frontend.route('/one_page_op_video_event_form')
def one_page_op_video_event_form():
    return render_template('sample_frontend/one-page/op-video-event-form.html')


@sample_frontend.route('/one_page_op_html5_video_light')
def one_page_op_html5_video_light():
    return render_template('sample_frontend/one-page/op-html5-video-light.html')


@sample_frontend.route('/one_page_op_big_text')
def one_page_op_big_text():
    return render_template('sample_frontend/one-page/op-big-text.html')


@sample_frontend.route('/one_page_op_revolution_fullwidth')
def one_page_op_revolution_fullwidth():
    return render_template('sample_frontend/one-page/op-revolution-fullwidth.html')


@sample_frontend.route('/one_page_op_cheermonk_fade_slider')
def one_page_op_cheermonk_fade_slider():
    return render_template('sample_frontend/one-page/op-cheermonk-fade-slider.html')

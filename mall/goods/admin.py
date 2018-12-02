from django.contrib import admin

from goods.models import Shop, Unit, Spu, Sku, ShopImage, Banner, Activity, ActivityArea, ActivityShop


# 分类商品
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_per_page = 5
    actions_on_top = True
    actions_on_bottom = True
    list_display = ['id', 'shop_username', 'shop_describe']
    list_display_links = ['id', 'shop_username']
    list_filter = ['shop_username']
    search_fields = ['shop_username']

    fieldsets = (
        ("分类名", {'fields': ("shop_username",)}),
        ("分类介绍", {'fields': ("shop_describe",)}),
    )


# 商品单位表
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_per_page = 5
    actions_on_top = True
    actions_on_bottom = True
    list_display = ['id', 'unit_name']
    list_display_links = ['id', 'unit_name']
    list_filter = ['unit_name']
    search_fields = ['unit_name']

    fieldsets = (
        ("单位名", {'fields': ("unit_name",)}),
    )


# 商品spu表
@admin.register(Spu)
class SpuAdmin(admin.ModelAdmin):
    list_per_page = 5
    actions_on_top = True
    actions_on_bottom = True
    list_display = ['id', 'spu_name', 'spu_details']
    list_display_links = ['id', 'spu_name']
    list_filter = ['spu_name']
    search_fields = ['spu_name']

    fieldsets = (
        ("名称", {'fields': ("spu_name",)}),
        ("详情", {'fields': ("spu_details",)}),
    )


# 商品sku表
class SkuAdminInline(admin.TabularInline):
    model = Sku  # 关联子对象


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    list_per_page = 5
    actions_on_top = True
    actions_on_bottom = True
    list_display = ['id', 'sku_trade_name',
                    'sku_introduce',
                    'sku_price',
                    'sku_unit_id',
                    'sku_stock',
                    'sku_Sales_volume',
                    'show_logo',
                    'sku_is_upper',
                    'sku_shop_id',
                    'sku_spu_id',
                    ]
    list_display_links = ['id', 'sku_trade_name']
    list_filter = ['sku_trade_name']
    search_fields = ['sku_trade_name']

    fieldsets = (
        ("商品名", {'fields': ("sku_trade_name",)}),
        ("简介", {'fields': ("sku_introduce",)}),
        ("价格", {'fields': ("sku_price",)}),
        ("单位id", {'fields': ("sku_unit_id",)}),
        ("库存", {'fields': ("sku_stock",)}),
        ("销量", {'fields': ("sku_Sales_volume",)}),
        ("logo地址", {'fields': ("sku_logo_address",)}),
        ("是否上架", {'fields': ("sku_is_upper",)}),
        ("商品分类id", {'fields': ("sku_shop_id",)}),
        ("商品spu_id", {'fields': ("sku_spu_id",)}),
    )


# 商品相册
@admin.register(ShopImage)
class ShopImageAdmin(admin.ModelAdmin):
    list_per_page = 5
    actions_on_top = True
    actions_on_bottom = True
    list_display = ['id', 'shopImage_image', 'shopImage_Sku_id']
    list_display_links = ['id', 'shopImage_image']
    list_filter = ['shopImage_image']
    search_fields = ['shopImage_image']

    fieldsets = (
        ("商品图片", {'fields': ("shopImage_image",)}),
        ("商品id", {'fields': ("shopImage_Sku_id",)}),
    )


# 首页轮播图
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_per_page = 5
    actions_on_top = True
    actions_on_bottom = True
    list_display = ['id', 'banner_name', 'banner_sku_id', 'banner_image', 'banner_order']
    list_display_links = ['id', 'banner_name']
    list_filter = ['banner_name']
    search_fields = ['banner_name']

    fieldsets = (
        ("名称", {'fields': ("banner_name",)}),
        ("商品id", {'fields': ("banner_sku_id",)}),
        ("图片", {'fields': ("banner_image",)}),
        ("排序", {'fields': ("banner_order",)}),
    )


# 首页活动表
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_per_page = 5
    actions_on_top = True
    actions_on_bottom = True
    list_display = ['id', 'activity_name', 'activity_image', 'activity_url']
    list_display_links = ['id', 'activity_name']
    list_filter = ['activity_name']
    search_fields = ['activity_name']

    fieldsets = (
        ("名称", {'fields': ("activity_name",)}),
        ("图片", {'fields': ("activity_image",)}),
        ("地址", {'fields': ("activity_url",)}),
    )


# 活动专区
@admin.register(ActivityArea)
class ActivityAreaAdmin(admin.ModelAdmin):
    list_per_page = 5
    actions_on_top = True
    actions_on_bottom = True
    list_display = ['id', 'ActivityArea_name', 'ActivityArea_describe', 'ActivityArea_order']
    list_display_links = ['id', 'ActivityArea_name']
    list_filter = ['ActivityArea_name']
    search_fields = ['ActivityArea_name']

    fieldsets = (
        ("名称", {'fields': ("ActivityArea_name",)}),
        ("描述", {'fields': ("ActivityArea_describe",)}),
        ("排序", {'fields': ("ActivityArea_order",)}),
    )


# 专区活动商品
@admin.register(ActivityShop)
class ActivityShopAdmin(admin.ModelAdmin):
    list_per_page = 5
    actions_on_top = True
    actions_on_bottom = True
    list_display = ['id', 'ActivityShop_ActivityArea_id', 'ActivityShop_sku_id']
    list_display_links = ['id', 'ActivityShop_ActivityArea_id']
    list_filter = ['ActivityShop_ActivityArea_id']
    search_fields = ['ActivityShop_ActivityArea_id']

    fieldsets = (
        ("活动专区id", {'fields': ("ActivityShop_ActivityArea_id",)}),
        ("商品id", {'fields': ("ActivityShop_sku_id",)}),
    )
package dev.nexreon.tfcmineralogy.init;

import net.minecraft.util.StringRepresentable;
import net.minecraft.world.level.material.MapColor;

enum ResourceEnums implements StringRepresentable {
    DIORITE("diorite"),
    GABBRO("gabbro"),
    SHALE("shale"),
    CLAYSTONE("claystone"),
    LIMESTONE("limestone"),
    CONGLOMERATE("conglomerate"),
    DOLOMITE("dolomite"),
    CHERT("chert"),
    CHALK("chalk"),
    RHYOLITE("rhyolite"),
    BASALT("basalt"),
    ANDESITE("andesite"),
    DACITE("dacite"),
    QUARTZITE("quartzite"),
    SLATE("slate"),
    PHYLLITE("phyllite"),
    SCHIST("schist"),
    GNEISS("gneiss"),
    MARBLE("marble");

    private final String name;

    ResourceEnums(String name) {
        this.name = name;
    }

    @Override
    public String getSerializedName() {
        return this.name;
    }
}
enum MineralType implements StringRepresentable {
    VIVIANITE("vivianite", MapColor.COLOR_GREEN, 6.5F, true),
    POOR_SMITHSONITE("poor_smithsonite", MapColor.COLOR_BLUE, 6.5f, true),
    NORMAL_SMITHSONITE("normal_smithsonite", MapColor.COLOR_BLUE, 6.5f, false),
    RICH_SMITHSONITE("rich_smithsonite", MapColor.COLOR_BLUE, 6.5f, false),
    REALGAR("realgar", MapColor.COLOR_ORANGE, 6.5f, true);

    private final String name;
    private final MapColor baseMapColor;
    private final float blockStrength;
    private final boolean hasDust;

    MineralType(String name, MapColor baseMapColor, float strength, boolean hasDust) {
        this.name = name;
        this.baseMapColor = baseMapColor;
        this.blockStrength = strength;
        this.hasDust = hasDust;
    }
    public boolean getHasDust(){
        return this.hasDust;
    }
    public float getBlockStrength(){
        return this.blockStrength;
    }
    @Override
    public String getSerializedName() {
        return this.name;
    }
    public MapColor getBaseMapColor() {
        return this.baseMapColor;
    }
}
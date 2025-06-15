package dev.nexreon.tfcm.common;

import java.util.List;

import javax.annotation.Nullable;

import net.dries007.tfc.common.TFCTags;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.ToolTier;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.Tiers;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.block.Block;
import net.minecraftforge.common.TierSortingRegistry;

public class TFCMTiers {
    // Code kept as a reference for the future:

    // Stone >= Vanilla Wood
    //public static final Tier IGNEOUS_INTRUSIVE = register("igneous_intrusive", Tiers.WOOD, Tiers.STONE, TFCTags.Blocks.NEEDS_STONE_TOOL, 0, 60, 4.7f, 2.0f, 5);
    
    // Copper >= Vanilla Stone
    //public static final Tier COPPER = register("copper", Tiers.STONE, Tiers.IRON, TFCTags.Blocks.NEEDS_COPPER_TOOL, 1, 600, 5.25f, 3.25f, 8);
    
    // Bronze >= Vanilla Iron
    public static final Tier ARSENICAL_BRONZE = register("arsenical_bronze", Tiers.IRON, Tiers.DIAMOND, TFCTags.Blocks.NEEDS_BRONZE_TOOL, 2, 1300, 7.3f, 4.0f, 13);
    public static final Tier CAST_IRON = register("cast_iron", Tiers.IRON, Tiers.DIAMOND, TFCTags.Blocks.NEEDS_BRONZE_TOOL, 2, 600, 7.3f, 4.0f, 13);
    //public static final Tier BRONZE = register("bronze", Tiers.IRON, Tiers.DIAMOND, TFCTags.Blocks.NEEDS_BRONZE_TOOL, 2, 1300, 7.3f, 4.0f, 13);
    
    // Wrought Iron >= Vanilla Iron
    //public static final Tier WROUGHT_IRON = register("wrought_iron", List.of(BRONZE, BISMUTH_BRONZE, BLACK_BRONZE, Tiers.IRON), List.of(Tiers.DIAMOND), TFCTags.Blocks.NEEDS_WROUGHT_IRON_TOOL, 3, 2200, 8.0f, 4.75f, 12);
    
    // Steel >= Vanilla Diamond
    //public static final Tier STEEL = register("steel", Tiers.DIAMOND, Tiers.NETHERITE, TFCTags.Blocks.NEEDS_STEEL_TOOL, 4, 3300, 9.5f, 5.75f, 12);
    
    // Black Steel >= Vanilla Diamond
    //public static final Tier BLACK_STEEL = register("black_steel", STEEL, Tiers.NETHERITE, TFCTags.Blocks.NEEDS_BLACK_STEEL_TOOL, 5, 4200, 11.0f, 7.0f, 17);
    
    // Colored Steel >= Vanilla Netherite
    //public static final Tier BLUE_STEEL = register("blue_steel", Tiers.NETHERITE, null, TFCTags.Blocks.NEEDS_COLORED_STEEL_TOOL, 6, 6500, 12.0f, 9.0f, 22);

    private static Tier register(String name, Tier before, @Nullable Tier after, TagKey<Block> tag, int level, int uses, float speed, float damage, int enchantmentValue)
    {
        return register(name, List.of(before), after == null ? List.of() : List.of(after), tag, level, uses, speed, damage, enchantmentValue);
    }

    private static Tier register(String name, List<Object> before, List<Object> after, TagKey<Block> tag, int level, int uses, float speed, float damage, int enchantmentValue)
    {
        final Tier tier = new ToolTier(name, level, uses, speed, damage, enchantmentValue, tag, () -> Ingredient.EMPTY);
        if (!Helpers.BOOTSTRAP_ENVIRONMENT) TierSortingRegistry.registerTier(tier, Helpers.identifier(name), before, after);
        return tier;
    }
}

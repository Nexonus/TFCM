package dev.nexreon.tfcm.util;

import java.util.Locale;
import java.util.Objects;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;

import javax.annotation.Nullable;

import dev.nexreon.tfcm.common.blocks.TFCMBlocks;
import net.dries007.tfc.common.TFCTags;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.common.blocks.ExtendedProperties;
import net.dries007.tfc.common.blocks.TFCBlocks;
import net.dries007.tfc.common.blocks.TFCChainBlock;
import net.dries007.tfc.common.blocks.devices.AnvilBlock;
import net.dries007.tfc.common.blocks.devices.LampBlock;
import net.dries007.tfc.common.items.ChiselItem;
import net.dries007.tfc.common.items.HammerItem;
import net.dries007.tfc.common.items.IngotItem;
import net.dries007.tfc.common.items.JavelinItem;
import net.dries007.tfc.common.items.LampBlockItem;
import net.dries007.tfc.common.items.MaceItem;
import net.dries007.tfc.common.items.PropickItem;
import net.dries007.tfc.common.items.ScytheItem;
import net.dries007.tfc.common.items.TFCFishingRodItem;
import net.dries007.tfc.common.items.TFCHoeItem;
import net.dries007.tfc.common.items.TFCShieldItem;
import net.dries007.tfc.common.items.ToolItem;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.Metal.Tier;
import net.dries007.tfc.util.registry.RegistryMetal;
import net.minecraft.util.Mth;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.HorseArmorItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.PickaxeItem;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.ShearsItem;
import net.minecraft.world.item.ShovelItem;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.TieredItem;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.IronBarsBlock;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.TrapDoorBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.BlockSetType;
import net.minecraft.world.level.block.state.properties.NoteBlockInstrument;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;

public final class TFCMMetal{ 
    public enum Default implements RegistryMetal{
    LEAD(0xFF66656c, MapColor.COLOR_GRAY, Rarity.COMMON, true, false, false);

    private final String serializedName;
    private final boolean parts, armor, utility;
    private final Tier metalTier;
    @Nullable private final net.minecraft.world.item.Tier toolTier;
    @Nullable private final ArmorMaterial armorTier;
    private final MapColor mapColor;
    private final Rarity rarity;
    private final int color;

    Default(int color, MapColor mapColor, Rarity rarity, boolean parts, boolean armor, boolean utility)
    {
        this(color, mapColor, rarity, Tier.TIER_0, null, null, parts, armor, utility);
    }

    Default(int color, MapColor mapColor, Rarity rarity, Tier metalTier, @Nullable net.minecraft.world.item.Tier toolTier, @Nullable ArmorMaterial armorTier, boolean parts, boolean armor, boolean utility)
    {
        this.serializedName = name().toLowerCase(Locale.ROOT);
        this.metalTier = metalTier;
        this.toolTier = toolTier;
        this.armorTier = armorTier;
        this.rarity = rarity;
        this.mapColor = mapColor;
        this.color = color;

        this.parts = parts;
        this.armor = armor;
        this.utility = utility;
    }
    @Override
        public String getSerializedName()
        {
            return serializedName;
        }

        public int getColor()
        {
            return color;
        }

        public Rarity getRarity()
        {
            return rarity;
        }

        public boolean hasParts()
        {
            return parts;
        }

        public boolean hasArmor()
        {
            return armor;
        }

        public boolean hasTools()
        {
            return toolTier != null;
        }

        public boolean hasUtilities()
        {
            return utility;
        }

        @Override
        public net.minecraft.world.item.Tier toolTier()
        {
            return Objects.requireNonNull(toolTier, "Tried to get non-existent tier from " + name());
        }

        @Override
        public ArmorMaterial armorTier()
        {
            return Objects.requireNonNull(armorTier, "Tried to get non-existent armor tier from " + name());
        }

        @Override
        public Tier metalTier()
        {
            return metalTier;
        }

        @Override
        public MapColor mapColor()
        {
            return mapColor;
        }

        @Override
        public Supplier<Block> getFullBlock()
        {
            return TFCMBlocks.METALS.get(this).get(BlockType.BLOCK);
        }
    }// May implement RegistryMetal, but cannot extend TFC.Metal
    public enum BlockType
    {
        ANVIL(Type.UTILITY, metal -> new AnvilBlock(ExtendedProperties.of().mapColor(metal.mapColor()).noOcclusion().sound(SoundType.ANVIL).strength(10, 10).requiresCorrectToolForDrops().blockEntity(TFCBlockEntities.ANVIL), metal.metalTier())),
        BLOCK(Type.PART, metal -> new Block(BlockBehaviour.Properties.of().mapColor(metal.mapColor()).instrument(NoteBlockInstrument.IRON_XYLOPHONE).requiresCorrectToolForDrops().strength(5.0F, 6.0F).sound(SoundType.METAL))),
        BLOCK_SLAB(Type.PART, metal -> new SlabBlock(BlockBehaviour.Properties.of().mapColor(metal.mapColor()).instrument(NoteBlockInstrument.IRON_XYLOPHONE).requiresCorrectToolForDrops().strength(5.0F, 6.0F).sound(SoundType.METAL))),
        BLOCK_STAIRS(Type.PART, metal -> new StairBlock(() -> metal.getFullBlock().get().defaultBlockState(), BlockBehaviour.Properties.of().mapColor(metal.mapColor()).instrument(NoteBlockInstrument.IRON_XYLOPHONE).requiresCorrectToolForDrops().strength(5.0F, 6.0F).sound(SoundType.METAL))),
        BARS(Type.UTILITY, metal -> new IronBarsBlock(BlockBehaviour.Properties.of().mapColor(metal.mapColor()).requiresCorrectToolForDrops().strength(6.0F, 7.0F).sound(SoundType.METAL).noOcclusion())),
        CHAIN(Type.UTILITY, metal -> new TFCChainBlock(Block.Properties.of().mapColor(metal.mapColor()).requiresCorrectToolForDrops().strength(5, 6).sound(SoundType.CHAIN).lightLevel(TFCBlocks.lavaLoggedBlockEmission()))),
        LAMP(Type.UTILITY, metal -> new LampBlock(ExtendedProperties.of().mapColor(metal.mapColor()).noOcclusion().sound(SoundType.LANTERN).strength(4, 10).randomTicks().pushReaction(PushReaction.DESTROY).lightLevel(state -> state.getValue(LampBlock.LIT) ? 15 : 0).blockEntity(TFCBlockEntities.LAMP)), (block, properties) -> new LampBlockItem(block, properties.stacksTo(1))),
        TRAPDOOR(Type.UTILITY, metal -> new TrapDoorBlock(Block.Properties.of().mapColor(metal.mapColor()).requiresCorrectToolForDrops().strength(5.0F).sound(SoundType.METAL).noOcclusion().isValidSpawn(TFCBlocks::never), BlockSetType.IRON));

        private final Function<RegistryMetal, Block> blockFactory;
        private final BiFunction<Block, Item.Properties, ? extends BlockItem> blockItemFactory;
        private final Type type;
        private final String serializedName;

        BlockType(Type type, Function<RegistryMetal, Block> blockFactory, BiFunction<Block, Item.Properties, ? extends BlockItem> blockItemFactory)
        {
            this.type = type;
            this.blockFactory = blockFactory;
            this.blockItemFactory = blockItemFactory;
            this.serializedName = name().toLowerCase(Locale.ROOT);
        }

        BlockType(Type type, Function<RegistryMetal, Block> blockFactory)
        {
            this(type, blockFactory, BlockItem::new);
        }

        public Supplier<Block> create(RegistryMetal metal)
        {
            return () -> blockFactory.apply(metal);
        }

        public Function<Block, BlockItem> createBlockItem(Item.Properties properties)
        {
            return block -> blockItemFactory.apply(block, properties);
        }

        public boolean has(Default metal)
        {
            return type.hasType(metal);
        }

        public String createName(RegistryMetal metal)
        {
            if (this == BLOCK_SLAB || this == BLOCK_STAIRS)
            {
                return BLOCK.createName(metal) + (this == BLOCK_SLAB ? "_slab" : "_stairs");
            }
            else
            {
                return "metal/" + serializedName + "/" + metal.getSerializedName();
            }
        }
    }

    public enum ItemType
    {
        // Generic
        INGOT(Type.DEFAULT, true, metal -> new IngotItem(properties(metal))),
        DOUBLE_INGOT(Type.PART, false),
        SHEET(Type.PART, false),
        DOUBLE_SHEET(Type.PART, false),
        ROD(Type.PART, false),
        TUYERE(Type.TOOL, metal -> new TieredItem(metal.toolTier(), properties(metal))),
        FISH_HOOK(Type.TOOL, false),
        FISHING_ROD(Type.TOOL, metal -> new TFCFishingRodItem(properties(metal).defaultDurability(metal.toolTier().getUses()), metal.toolTier())),
        UNFINISHED_LAMP(Type.UTILITY, metal -> new Item(properties(metal))),

        // Tools and Tool Heads
        PICKAXE(Type.TOOL, metal -> new PickaxeItem(metal.toolTier(), (int) ToolItem.calculateVanillaAttackDamage(0.75f, metal.toolTier()), -2.8F, properties(metal))),
        PICKAXE_HEAD(Type.TOOL, true),
        PROPICK(Type.TOOL, metal -> new PropickItem(metal.toolTier(), ToolItem.calculateVanillaAttackDamage(0.5f, metal.toolTier()), -2.8F, properties(metal))),
        PROPICK_HEAD(Type.TOOL, true),
        AXE(Type.TOOL, metal -> new AxeItem(metal.toolTier(), ToolItem.calculateVanillaAttackDamage(1.5f, metal.toolTier()), -3.1F, properties(metal))),
        AXE_HEAD(Type.TOOL, true),
        SHOVEL(Type.TOOL, metal -> new ShovelItem(metal.toolTier(), ToolItem.calculateVanillaAttackDamage(0.875F, metal.toolTier()), -3.0F, properties(metal))),
        SHOVEL_HEAD(Type.TOOL, true),
        HOE(Type.TOOL, metal -> new TFCHoeItem(metal.toolTier(), -1, -2f, properties(metal))),
        HOE_HEAD(Type.TOOL, true),
        CHISEL(Type.TOOL, metal -> new ChiselItem(metal.toolTier(), ToolItem.calculateVanillaAttackDamage(0.27f, metal.toolTier()), -1.5F, properties(metal))),
        CHISEL_HEAD(Type.TOOL, true),
        HAMMER(Type.TOOL, metal -> new HammerItem(metal.toolTier(), ToolItem.calculateVanillaAttackDamage(1f, metal.toolTier()), -3, properties(metal), metal.getSerializedName())),
        HAMMER_HEAD(Type.TOOL, true),
        SAW(Type.TOOL, metal -> new AxeItem(metal.toolTier(), ToolItem.calculateVanillaAttackDamage(0.5f, metal.toolTier()), -3, properties(metal))),
        SAW_BLADE(Type.TOOL, true),
        JAVELIN(Type.TOOL, metal -> new JavelinItem(metal.toolTier(), ToolItem.calculateVanillaAttackDamage(0.7f, metal.toolTier()), 1.5f * metal.toolTier().getAttackDamageBonus(), -2.6F, properties(metal), metal.getSerializedName())),
        JAVELIN_HEAD(Type.TOOL, true),
        SWORD(Type.TOOL, metal -> new SwordItem(metal.toolTier(), (int) ToolItem.calculateVanillaAttackDamage(1f, metal.toolTier()), -2.4F, properties(metal))),
        SWORD_BLADE(Type.TOOL, true),
        MACE(Type.TOOL, metal -> new MaceItem(metal.toolTier(), (int) ToolItem.calculateVanillaAttackDamage(1.3f, metal.toolTier()), -3, properties(metal))),
        MACE_HEAD(Type.TOOL, true),
        KNIFE(Type.TOOL, metal -> new ToolItem(metal.toolTier(), ToolItem.calculateVanillaAttackDamage(0.6f, metal.toolTier()), -2.0F, TFCTags.Blocks.MINEABLE_WITH_KNIFE, properties(metal))),
        KNIFE_BLADE(Type.TOOL, true),
        SCYTHE(Type.TOOL, metal -> new ScytheItem(metal.toolTier(), ToolItem.calculateVanillaAttackDamage(0.7f, metal.toolTier()), -3.2F, TFCTags.Blocks.MINEABLE_WITH_SCYTHE, properties(metal))),
        SCYTHE_BLADE(Type.TOOL, true),
        SHEARS(Type.TOOL, metal -> new ShearsItem(properties(metal).defaultDurability(metal.toolTier().getUses()))),

        // Armor
        UNFINISHED_HELMET(Type.ARMOR, false),
        HELMET(Type.ARMOR, metal -> new ArmorItem(metal.armorTier(), ArmorItem.Type.HELMET, properties(metal))),
        UNFINISHED_CHESTPLATE(Type.ARMOR, false),
        CHESTPLATE(Type.ARMOR, metal -> new ArmorItem(metal.armorTier(), ArmorItem.Type.CHESTPLATE, properties(metal))),
        UNFINISHED_GREAVES(Type.ARMOR, false),
        GREAVES(Type.ARMOR, metal -> new ArmorItem(metal.armorTier(), ArmorItem.Type.LEGGINGS, properties(metal))),
        UNFINISHED_BOOTS(Type.ARMOR, false),
        BOOTS(Type.ARMOR, metal -> new ArmorItem(metal.armorTier(), ArmorItem.Type.BOOTS, properties(metal))),
        HORSE_ARMOR(Type.ARMOR, metal -> new HorseArmorItem(Mth.floor(metal.armorTier().getDefenseForType(ArmorItem.Type.CHESTPLATE) * 1.5), Helpers.identifier("textures/entity/animal/horse_armor/" + metal.getSerializedName() + ".png"), properties(metal))),

        SHIELD(Type.TOOL, metal -> new TFCShieldItem(metal.toolTier(), properties(metal)));

        public static Item.Properties properties(RegistryMetal metal)
        {
            return new Item.Properties().rarity(metal.getRarity());
        }

        private final Function<RegistryMetal, Item> itemFactory;
        private final Type type;
        private final boolean mold;

        ItemType(Type type, boolean mold)
        {
            this(type, mold, metal -> new Item(properties(metal)));
        }

        ItemType(Type type, Function<RegistryMetal, Item> itemFactory)
        {
            this(type, false, itemFactory);
        }

        ItemType(Type type, boolean mold, Function<RegistryMetal, Item> itemFactory)
        {
            this.type = type;
            this.mold = mold;
            this.itemFactory = itemFactory;
        }

        public Item create(RegistryMetal metal)
        {
            return itemFactory.apply(metal);
        }

        public boolean has(Default metal)
        {
            return type.hasType(metal);
        }

        public boolean hasMold()
        {
            return mold;
        }
    }

    private enum Type
    {
        DEFAULT(metal -> true),
        PART(Default::hasParts),
        TOOL(Default::hasTools),
        ARMOR(Default::hasArmor),
        UTILITY(Default::hasUtilities);

        private final Predicate<TFCMMetal.Default> predicate;

        Type(Predicate<TFCMMetal.Default> predicate)
        {
            this.predicate = predicate;
        }

        boolean hasType(TFCMMetal.Default metal)
        {
            return predicate.test(metal);
        }
    }
}

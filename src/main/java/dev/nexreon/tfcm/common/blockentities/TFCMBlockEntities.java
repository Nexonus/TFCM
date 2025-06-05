package dev.nexreon.tfcm.common.blockentities;

import java.util.function.Supplier;
import java.util.stream.Stream;

import dev.nexreon.tfcm.TFCMineralogy;
import dev.nexreon.tfcm.common.blocks.TFCMBlocks;
import dev.nexreon.tfcm.util.TFCMMetal;

import net.dries007.tfc.common.blockentities.IngotPileBlockEntity;
import net.dries007.tfc.common.blockentities.SheetPileBlockEntity;

import net.dries007.tfc.util.registry.RegistrationHelpers;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

public class TFCMBlockEntities{
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES = DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, TFCMineralogy.MODID);
    public static final RegistryObject<BlockEntityType<SheetPileBlockEntity>> SHEET_PILE = register("tfcm_sheet_pile", SheetPileBlockEntity::new, TFCMBlocks.SHEET_PILE);
    public static final RegistryObject<BlockEntityType<IngotPileBlockEntity>> INGOT_PILE = register("tfcm_ingot_pile", IngotPileBlockEntity::new, Stream.of(TFCMBlocks.INGOT_PILE, TFCMBlocks.DOUBLE_INGOT_PILE));
    public static final RegistryObject<BlockEntityType<TFCMLampBlockEntity>> LAMP = register("tfcm_lamp", TFCMLampBlockEntity::new, TFCMBlocks.METALS.values().stream().filter(map -> map.get(TFCMMetal.BlockType.LAMP) != null).map(map -> map.get(TFCMMetal.BlockType.LAMP)));

    private static <T extends BlockEntity> RegistryObject<BlockEntityType<T>> register(String name, BlockEntityType.BlockEntitySupplier<T> factory, Supplier<? extends Block> block)
    {
        return RegistrationHelpers.register(BLOCK_ENTITIES, name, factory, block);
    }

    private static <T extends BlockEntity> RegistryObject<BlockEntityType<T>> register(String name, BlockEntityType.BlockEntitySupplier<T> factory, Stream<? extends Supplier<? extends Block>> blocks)
    {
        return RegistrationHelpers.register(BLOCK_ENTITIES, name, factory, blocks);
    }
}

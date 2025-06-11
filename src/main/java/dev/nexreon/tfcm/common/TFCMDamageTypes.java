package dev.nexreon.tfcm.common;

import dev.nexreon.tfcm.TFCMineralogy;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.damagesource.DamageType;

public class TFCMDamageTypes {
    @SuppressWarnings("removal")
    public static final ResourceKey<DamageType> FALLING_LEAD_BLOCK = 
        ResourceKey.create(Registries.DAMAGE_TYPE, new ResourceLocation(TFCMineralogy.MODID, "falling_lead_block"));
}
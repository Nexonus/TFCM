package dev.nexreon.tfcm.common;

import net.dries007.tfc.util.Helpers;

import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageType;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;

public class TFCMDamageSources {
    public static final ResourceKey<DamageType> FALLING_LEAD_BLOCK = ResourceKey.create(Registries.DAMAGE_TYPE, Helpers.identifier("falling_lead_block"));
    public static void falling_lead_block(Entity entity, float amount)
    {
        entity.hurt(new DamageSource(fetch(FALLING_LEAD_BLOCK, entity.level())), amount);
    }
    private static Holder<DamageType> fetch(ResourceKey<DamageType> type, Level level)
    {
        return level.registryAccess().registryOrThrow(Registries.DAMAGE_TYPE).getHolderOrThrow(type);
    }
}

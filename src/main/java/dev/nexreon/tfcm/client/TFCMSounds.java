package dev.nexreon.tfcm.client;

import java.util.Map;

import dev.nexreon.tfcm.TFCMineralogy;
import dev.nexreon.tfcm.common.TFCMArmorMaterials;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.registries.Registries;
import net.minecraft.sounds.SoundEvent;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

public class TFCMSounds {
    public static final DeferredRegister<SoundEvent> SOUNDS = DeferredRegister.create(Registries.SOUND_EVENT, TFCMineralogy.MODID);
    public static final Map<TFCMArmorMaterials, RegistryObject<SoundEvent>> ARMOR_EQUIP = Helpers.mapOfKeys(TFCMArmorMaterials.class, mat -> create("item.armor.equip_" + mat.getId().getPath()));
    private static RegistryObject<SoundEvent> create(String name)
    {
        return SOUNDS.register(name, () -> SoundEvent.createVariableRangeEvent(Helpers.identifier(name)));
    }

}

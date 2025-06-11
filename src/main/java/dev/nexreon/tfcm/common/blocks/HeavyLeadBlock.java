package dev.nexreon.tfcm.common.blocks;

import net.dries007.tfc.client.TFCSounds;
import net.dries007.tfc.common.blocks.rock.IFallableBlock;
import net.dries007.tfc.common.entities.misc.TFCFallingBlockEntity;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.entity.item.FallingBlockEntity;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.FallingBlock;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.DirectionProperty;
import net.minecraft.world.level.pathfinder.PathComputationType;

public class HeavyLeadBlock extends FallingBlock implements IFallableBlock{

   public static final DirectionProperty FACING = HorizontalDirectionalBlock.FACING;

    public HeavyLeadBlock(BlockBehaviour.Properties properties) {
      super(properties);
      this.registerDefaultState(this.stateDefinition.any().setValue(FACING, Direction.NORTH));
   }
   @Override
   public void onPlace(BlockState blockState, Level level, BlockPos blockPos, BlockState p_53236_, boolean p_53237_) {
      level.scheduleTick(blockPos, this, this.getDelayAfterPlace());
   }
   protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> blockState) {
      blockState.add(FACING);
   }
   public BlockState getStateForPlacement(BlockPlaceContext blockPlaceContext) {
      return this.defaultBlockState().setValue(FACING, blockPlaceContext.getHorizontalDirection().getOpposite());
   }

   public static boolean canFallThrough(BlockGetter world, BlockPos pos, BlockState state)
    {
        return !state.isFaceSturdy(world, pos, Direction.UP);
    }
   @Override
    public void onceFinishedFalling(Level level, BlockPos blockPos, FallingBlockEntity fallingBlock)
    {
         ((ServerLevel) level).sendParticles(ParticleTypes.CRIT,
         blockPos.getX() + 0.5, blockPos.getY() + 0.25, blockPos.getZ() + 0.5, 40, 0.0005, -0.005, 0.0005, 0.5);
         Helpers.playSound(level, blockPos, TFCSounds.ANVIL_HIT.get());
    }

   @Override
   public void tick(BlockState blockState, ServerLevel level, BlockPos blockPos, RandomSource randomSource) {
      if (isFree(level.getBlockState(blockPos.below())) && blockPos.getY() >= level.getMinBuildHeight()) {
         //FallingBlockEntity fallingblockentity = FallingBlockEntity.fall(level, blockPos, blockState);
         level.addFreshEntity(new TFCFallingBlockEntity(level, blockPos.getX() + 0.5, blockPos.getY(), blockPos.getZ() + 0.5, blockState, 4.5f, 50));
      }
   }
   public DamageSource getFallDamageSource(TFCFallingBlockEntity fallingEntity) {
      return new DamageSource(fallingEntity.level().registryAccess().registryOrThrow(Registries.DAMAGE_TYPE)
      .getHolderOrThrow(DamageTypes.FALLING_ANVIL),fallingEntity);
   }

   public boolean isPathfindable(BlockState state, BlockGetter level, BlockPos pos, PathComputationType type)
    {
        return false;
    }
}

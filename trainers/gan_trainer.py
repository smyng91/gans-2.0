import os
from abc import abstractmethod

import tensorflow as tf

from datasets import abstract_dataset
from utils import constants

SEED = 0


class GANTrainer:
    
    def __init__(
            self,
            batch_size,
            generator,
            discriminator,
            dataset_type,
            lr_generator,
            lr_discriminator,
            continue_training,
            checkpoint_step=10,
    ):
        self.batch_size = batch_size
        self.generator = generator
        self.discriminator = discriminator
        self.checkpoint_step = checkpoint_step
        self.dataset_type = dataset_type
        self.lr_generator = lr_generator
        self.lr_discriminator = lr_discriminator
        self.continue_training = continue_training
        
        self.generator_optimizer_a = tf.keras.optimizers.Adam(self.lr_generator, beta_1=0.5)
        self.generator_optimizer_b = tf.keras.optimizers.Adam(self.lr_generator, beta_1=0.5)
        self.discriminator_optimizer_a = tf.keras.optimizers.Adam(self.lr_discriminator, beta_1=0.5)
        self.discriminator_optimizer_b = tf.keras.optimizers.Adam(self.lr_discriminator, beta_1=0.5)
        
        self.checkpoint_path = os.path.join(
            constants.SAVE_IMAGE_DIR,
            dataset_type,
            constants.CHECKPOINT_DIR,
        )
        
        self.checkpoint_prefix = os.path.join(self.checkpoint_path, "ckpt")
        
        self.checkpoint = tf.train.Checkpoint(
            generator_optimizer_a=self.generator_optimizer_a,
            generator_optimizer_b=self.generator_optimizer_b,
            discriminator_optimizer_a=self.discriminator_optimizer_a,
            discriminator_optimizer_b=self.discriminator_optimizer_b,
            generator_a=self.generator[0].model,
            generator_b=self.generator[1].model,
            discriminator_a=self.discriminator[0].model,
            discriminator_b=self.discriminator[1].model,
        )
        self.summary_writer = tf.summary.create_file_writer(self.checkpoint_path)
    
    @abstractmethod
    def train(self, dataset: abstract_dataset.Dataset, num_epochs: int):
        raise NotImplementedError

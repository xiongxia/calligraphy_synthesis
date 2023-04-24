# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
import models.parser as parser
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from models.unet_onehot_cns_font_attention import UNet

# parser.add_argument('--model_dir', dest='model_dir',
#                     help='directory that saves the model checkpoints')
# parser.add_argument('--source_obj', dest='source_obj', type=str, help='the source images for inference')
# parser.add_argument('--embedding_ids', default='embedding_ids', type=str, help='embeddings involved')
# parser.add_argument('--save_dir', default='save_dir', type=str, help='path to save inferred images')
# parser.add_argument('--interpolate', dest='interpolate', type=int, default=0,
#                     help='interpolate between different embedding vectors')
# parser.add_argument('--steps', dest='steps', type=int, default=10, help='interpolation steps in between vectors')
# parser.add_argument('--uroboros', dest='uroboros', type=int, default=0,
#                     help='you have stepped into uncharted territory')

def main(_):
    args = parser.arg_parse()
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    with tf.Session(config=config) as sess:
        model = UNet(batch_size=1, embedding_num=args.embedding_num, cns_embedding_size=args.cns_embedding_size)
        model.register_session(sess)
        model.build_model(is_training=False, inst_norm=args.inst_norm)
        embedding_ids = [int(i) for i in args.embedding_ids.split(",")]
        if not args.interpolate:
            if len(embedding_ids) == 1:
                embedding_ids = embedding_ids[0]
            model.infer(model_dir=args.model_dir, source_obj=args.source_obj, embedding_ids=embedding_ids,
                        save_dir=args.save_dir)
        else:
            if len(embedding_ids) < 2:
                raise Exception("no need to interpolate yourself unless you are a narcissist")
            chains = embedding_ids[:]
            if args.uroboros:
                chains.append(chains[0])
            pairs = list()
            for i in range(len(chains) - 1):
                pairs.append((chains[i], chains[i + 1]))
            for s, e in pairs:
                model.interpolate(model_dir=args.model_dir, source_obj=args.source_obj, between=[s, e],
                                  save_dir=args.save_dir, steps=args.steps)


if __name__ == '__main__':
    tf.app.run()

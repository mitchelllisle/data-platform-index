# coding=utf-8
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


class MyOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            '--output',
            default='./output.txt',
            help='Output for the pipeline')


if __name__ == '__main__':
    options = MyOptions()
    options.view_as(beam.options.pipeline_options.StandardOptions).runner = 'DirectRunner'

    p = beam.Pipeline(options=options)

    (p
     | 'create numbers' >> beam.Create([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
     | 'combine numbers' >> beam.CombineGlobally(sum)
     | 'write to text' >> beam.io.WriteToText(options.output, shard_name_template=""))

    p.run().wait_until_finish()

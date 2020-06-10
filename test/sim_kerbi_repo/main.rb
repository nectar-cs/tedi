require 'kerbi'

class SimpleMixer < Kerbi::Mixer
  locate_self __dir__
  def run
    super do |g|
      g.yaml 'svc'
    end
  end
end

kerbi.generators = [ SimpleMixer ]

puts kerbi.gen_yaml
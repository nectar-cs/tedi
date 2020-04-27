require 'kerbi'

class SimpleGen < Kerbi::Gen
  locate_self __dir__
  def gen
    safe_gen do |res|
      res.yaml 'svc'
    end
  end
end

kerbi.generators = [ SimpleGen ]

puts kerbi.gen_yaml
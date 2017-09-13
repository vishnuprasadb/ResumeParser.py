class ResumeXmlHandler(xml.sax.ContentHandler):

        def __init__(self):
                self.node = ''
                self.params = {}
                self.error = None
        def startElement(self, name, attrs):
                self.node = name
        def endElement(self, name):
                self.node = ''
        def characters(self,content):
                if self.node == 'Summary':
                        for dirty in ['Work Sumamry','WORK SUMMARY','Summary','Professional Summary','PROFESSIONAL','Professional:','PROFESSIONAL:','PROFESSIONAL :','PROFESSIONAL SUMMARY:','Professional summary','SUMMARY','PROFESSIONAL SUMMARY','SUMMARY:','EXECUTIVE SUMMARY']:
                                if dirty in content:
                                        content=content.replace(dirty,'')
                        if self.params.has_key(self.node.lower()):
                                self.params[self.node.lower()] += _my_unescape(content)
                        else:
                                self.params[self.node.lower()] = _my_unescape(content)
                else:
                        content=content.strip()

                if self.node == 'ResumeFileName':
                        self.params['resumefilename'] = _my_unescape(content)
                elif self.node == 'FirstName':
                        self.params[self.node.lower()] = _my_unescape(content)
                elif self.node == 'LastName':
                        self.params[self.node.lower()] = _my_unescape(content)
                elif self.node == 'Email':
                        for dirty in ['E-mail-','-',':-',':',' ']:
                                if dirty in content:
                                        content=content.split(dirty)[1]
                        self.params[self.node.lower()] = _my_unescape(content.strip())
                elif self.node == 'Phone' or self.node == 'Mobile' or self.node == 'FormattedPhone' or self.node =='FormattedMobile':
                        content=content.replace(' ','')
                        if len(content)>10:
                                self.params[self.node.lower()] = _my_unescape(content)[-10:]
                        elif len(content)<10:
                                pass
                        else:
                                self.params[self.node.lower()] = _my_unescape(content)
                elif self.node == 'Address':
                        self.params[self.node.lower()] = _my_unescape(content)
                elif self.node == 'City':
                        self.params[self.node.lower()] = _my_unescape(content)
                elif self.node == 'State':
                        self.params[self.node.lower()] = _my_unescape(content)
                elif self.node == 'ZipCode':
                        self.params['pincode'] = _my_unescape(content)
                elif self.node == 'Skill':
                        skill_list = _my_unescape(content).replace('\n', ',').replace('\r', '').split(',')
                        labels = ['language', 'frameworks', 'tools', 'operating systems','training','analysis','module','user interface','programming','trouble shooting','capability','specifications','platforms','modules','cleanliness','assembly']
                        self.params['claimed_skills'] = ''
                        for skill in skill_list:
                                skill = skill.strip()
                                if skill.lower() not in labels:
                                        self.params['claimed_skills'] += 's_%s,'%skill
                # candidate profile fields
                elif self.node == 'Gender':
                        gender_dict={'Female':'F',
                                     'Male':'M',
                                     'Other':'O'
                                    }
                        gender=_my_unescape(content)
      
                        if gender in gender_dict.keys():
                                self.params[self.node.lower()] = gender_dict[gender]
                elif self.node =='DateOfBirth':
                        self.params[self.node.lower()] = _parse_date(_my_unescape(content))
                elif self.node == 'LicenseNo':
                        self.params[self.node.lower()] = _my_unescape(content)
                elif self.node == 'Nationality':
                        self.params[self.node.lower()] = _my_unescape(content)
#End of ResumeXmlHandler()

def _parse_date(data):
        if data.count('/') ==2:
                DOB = data.split('/')
                date_of_birth = '%s-%s-%s'%(DOB[2],DOB[1],DOB[0])
        else:
                date_of_birth =''
        return date_of_birth

class ProfileFieldsSanitizer(file):

        def __init__(self,file):
                self.invalid_fields = {}
                self.filename = file

        _NAMEVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 150,
        }

        _EMAILVALIDATOR = {
                'type': 'str',
                'regex': '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                'maxlen': 30,
        }
        _PHONEVALIDATOR = {
                'type': 'str',
                'regex': '^\+?1?\d{9,15}$',
                'maxlen': 15,
        }
        _ADDRVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 128,
        }
        _CITYVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 64,
        }
        _STATEVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 64,
        }
        _PINVALIDATOR = {
                'type': 'int',
                'regex': '\d{5,6}',
                'maxval': 999999,
                'minval': 0,
        }
        _CLAIMEDSKILLVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 8192,
        }
        _GENDERVALIDATOR = {
                'type': 'str',
                'regex': '[FMO]',
                'maxlen': 1,
        }
        _DOBVALIDATOR = {
                'type': 'str',
                'regex': '\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])',
                'maxlen': 10,
        }
        _LICENSEVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 512,
        }
        _SUMMARYVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 4096,
        }
        _CTCVALIDATOR = {
                'type': 'float',
                'regex': '.*',
                'maxval': 9999999999.99,
                'minval': 0,
        }
        _NPVALIDATOR = {
                'type': 'int',
                'regex': '.*',
                'maxval': 12,
                'minval': -1,
        }
        _DEGREEVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 16,
        }
        _BRANCHVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 32,
        }
        _COLLEGEVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 128,
        }
        _UNIVERSITYVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 128,
        }
        _DEGREEYEARVALIDATOR = {
                'type': 'int',
                'regex': '.*',
                'maxval': 1947,
                'minval': 2100,
        }
        _PERFORMANCEVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 128,
        }
        _EMPLOYERVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 64,
        }
        _ROLEVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 1024,
        }
        _JOBLOCATIONVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 64,
        }
        _JOBDATEVALIDATOR = {
                'type': 'str',
                'regex': '\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])',
                'maxlen': 10,
        }
        _JOBPERIODVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 64,
        }
        _JDVALIDATOR = {
                'type': 'str',
                'regex': '.*',
                'maxlen': 8192,
        }

        _validators = {

                'firstname': _NAMEVALIDATOR,
                'lastname': _NAMEVALIDATOR,
                'email': _EMAILVALIDATOR,
                'phone': _PHONEVALIDATOR,
                'address': _ADDRVALIDATOR,
                'address1': _ADDRVALIDATOR,
                'address2': _ADDRVALIDATOR,
                'city': _CITYVALIDATOR,
                'state': _STATEVALIDATOR,
                'pincode': _PINVALIDATOR,
                'claimed_skills': _CLAIMEDSKILLVALIDATOR,
                'gender': _GENDERVALIDATOR,
                'dateofbirth': _DOBVALIDATOR,
                'birthdate': _DOBVALIDATOR,
                'licenseno': _LICENSEVALIDATOR,
                'dl_number': _LICENSEVALIDATOR,
                'summary': _SUMMARYVALIDATOR,
                'annualCtc': _CTCVALIDATOR,
                'annualctc': _CTCVALIDATOR,
                'expectedCtc': _CTCVALIDATOR,
                'expectedctc': _CTCVALIDATOR,
                'curSalary': _CTCVALIDATOR,
                'expSalary': _CTCVALIDATOR,
                'noticePeriod': _NPVALIDATOR,
                'degree': _DEGREEVALIDATOR,
                'branch': _BRANCHVALIDATOR,
                'college': _COLLEGEVALIDATOR,
                'university': _UNIVERSITYVALIDATOR,
                'year': _DEGREEYEARVALIDATOR,
                'joiningYear': _DEGREEYEARVALIDATOR,
                'graduationYear': _DEGREEYEARVALIDATOR,
                'performance': _PERFORMANCEVALIDATOR,
                'aggregate': _PERFORMANCEVALIDATOR,
                'employer': _EMPLOYERVALIDATOR,
                'jobprofile': _ROLEVALIDATOR,
                'joblocation': _JOBLOCATIONVALIDATOR,
                'startdate': _JOBDATEVALIDATOR,
                'enddate': _JOBDATEVALIDATOR,
                'jobperiod': _JOBPERIODVALIDATOR,
                'jobdescritption': _JDVALIDATOR,

        }

        def _validate(self, validator, key, value):
                if validator['type'] == 'str':
                        try:
                                value = str(value)
                        except:
                                self.invalid_fields[key] = value
                                return 'invalid'
                if validator['type'] == 'int':
                        try:
                                int(value)
                                value = str(value)
                        except:
                                self.invalid_fields[key] = value
                                return 'invalid'
                if validator['type'] == 'float':
                        try:
                                float(value)
                                value = str(value)
                        except:
                                self.invalid_fields[key] = value
                                return 'invalid'
                if not re.match(validator['regex'],value):
                        self.invalid_fields[key] = value
                        return 'invalid'
                if type(value) == 'string':
                        if validator['maxlen'] < len(value):
                                self.invalid_fields[key] = value
                                return 'invalid'
                elif type(value) in ['int' or 'float']:
                        if validator['maxval'] < value:
                                self.invalid_fields[key] = value
                                return 'invalid'
                        if validator['minval'] > value:
                                self.invalid_fields[key] = value
                                return 'invalid'

                return 'valid'

        def validate(self, name, value):

                validity = 'didnotvalidate'

                if self._validators.has_key(name):
                        validator = self._validators[name]
                        validity = self._validate(validator, name, value)

                if validity == 'invalid':
                        return False
                else:
                        return True

        def validate_all_fields(self, dict_in):
                for k in dict_in.keys():
                        value = dict_in[k]
                        if type(value) is not dict:
                                if not self.validate(k, value):
                                        dict_in[k] = None
                        else:
                                for i in value:
                                        if not self.validate(i, value[i]):
                                                dict_in[k][i] = None
                if self.invalid_fields:
                        f=open(self.filename,'w')
                        f.write('Field,Value\r\n')
                        for field in self.invalid_fields:
                                try:
                                        f.write('%s,%s\r\n'%(field,self.invalid_fields[field]))
                                except:
                                        f.write('%s\r\n'%(field))
                        f.close()
                else:
                        os.remove(self.filename)
# End of ProfileFieldsSanitizer()

#Resume parser using RChilli API
def _resume_parser(content_type,resume_data,err_resp=''):

        logr.info("Incoming request to parser resume using RChilli API")

        errors = ''

        valid_content_types = {'application/pdf': 'pdf', 'application/msword': 'doc' , 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.template':'dotx', 'application/vnd.ms-word.document.macroEnabled.12':'docm', 'application/vnd.ms-word.template.macroEnabled.12':'dotm'}
        if content_type not in valid_content_types.keys() :
                logr.info("Invalid content type-%s"%content_type)
                errors += 'Invalid value (%s) for the field %s'%(content_type,"Content Type")
                err_resp += '<errors>\r\n'
                err_resp += _add_xml_field('errorStr',errors)
                err_resp += '</errors>\r\n'
                return ({},err_resp)
        else:
                pid=os.getpid()
                filename = 'resume_%s.%s'%(pid,valid_content_types[content_type])
        data = resume_data.split('#')[0]
        decoded_data= b64decode(data)
        f = open('/tmp/%s'%filename,'w')
        f.write(decoded_data)
        f.close()

        # Dictionary for storing candidate info
        # Key : model fields
        # Value: the data

        cand_res_data={}
        cand_res_data['filename']=filename
        retval = call(['/var/floLearning/RChilliParser/parser.sh',filename])
        if retval != 0:
                errors += "Error while parsing %s"%filename
                err_resp += _add_xml_field("errorStr",errors)
                return (cand_res_data,err_resp)

        output_fn= '/content/candidates/resume_responses/xml_resp_%s.txt'%filename
        with open(output_fn,'r') as f_name:
                xmldata = f_name.read()

        xmlhandler = ResumeXmlHandler()
        error_file = 'errors_%s.txt'%pid
        retval = call(['touch','/content/candidates/resume_responses/errors/%s'%error_file])
        sanitizer = ProfileFieldsSanitizer('/content/candidates/resume_responses/errors/%s'%error_file)
        try:
                xml.sax.parseString(xmldata,xmlhandler)
        except Exception as e:
                errors += 'Error while parsing (SAX) %s\r\n'%filename
                err_resp += _add_xml_field('errorStr',errors)
                return (cand_res_data,err_resp)
        cand_resume_data = xmlhandler
        sanitizer.validate_all_fields(cand_resume_data.params)
        cand_resume_data.params['error_file'] = error_file
        cand_resume_data.params['filename'] = filename
        cand_resume_data.params['rchillie_resp_file']='xml_resp_%s.txt'%filename

        logr.info(cand_resume_data.params)

        return (cand_resume_data.params,err_resp)

#end of _resume_parser

def _update_parsed_candidate_profile_helper(candidate_resume_data,candidate):
        """
        Use case: This helper is used to update the candidate profile using the dictionary which contains the keys as model object fields and values as the respective data, got from the resume parser.
        input: dictionary of resume parsed info
        output: saving the data and returning the response of respective fields which are updated
        
        """
        logr.info("Incoming data to update the candidate profile from resume parser output")

        addr = candidate_resume_data.get('address',0)
        city = candidate_resume_data.get('city',0)
        state = candidate_resume_data.get('state',0)
        pincode = candidate_resume_data.get('pincode',0)
        claimed_skills= candidate_resume_data.get('claimed_skills',0)
        gender = candidate_resume_data.get('gender',0)
        dateofbirth= candidate_resume_data.get('dateofbirth',0)
        licenseno = candidate_resume_data.get('licenseno',0)
        summary = candidate_resume_data.get('summary',0)
        nationality = candidate_resume_data.get('nationality',0)

        candidate_dirty = addr_dirty = False
        cand_addr, ignore = CurrentAddress.objects.get_or_create(candidate_id = candidate.id)
        if addr:
                addr_dirty = True
                cand_addr.address1 = addr
        if city:
                addr_dirty = True
                cand_addr.city= city
        if state:
                addr_dirty = True
                cand_addr.state= state
        if pincode:
                addr_dirty = True
                cand_addr.pin_code= pincode
        if claimed_skills:
                candidate_dirty = True
                candidate.claimed_skills= claimed_skills
        if candidate_dirty:
                candidate.save()
        if addr_dirty:
                cand_addr.save()

        # Saving candidate profile
        candidate_profile = Profile.objects.get(candidate_id=candidate.id)
        profile_dirty = False
        if gender:
                profile_dirty = True
                candidate_profile.gender = gender
        if dateofbirth:
                profile_dirty = True
                candidate_profile.birthdate = dateofbirth
        if licenseno:
                profile_dirty = True
                candidate_profile.dl_number = licenseno
        if nationality:
                profile_dirty = True
                candidate_profile.nationality = nationality
        if summary:
                profile_dirty = True
                candidate_profile.summary = summary
        if profile_dirty:
                candidate_profile.save()
# End of _update_parsed_candidate_profile_helper


def _response_builder_from_parsed_resume_data(candidate,candidate_resume_data,resp):
        """
        builds the response from the parsed resume info dictionary
        """
        indent =3
        resp += '\t\t<newProfile>\r\n'
        resp += _add_xml_field("id", candidate.id,indent)
        resp += _add_xml_field("email", candidate.user.email,indent)
        resp += _add_xml_field("firstName", candidate.user.first_name,indent)
        resp += _add_xml_field("middleName", candidate.middle_name,indent)
        resp += _add_xml_field("lastName", candidate.user.last_name,indent)
        resp += _add_xml_field("mobileNumber", candidate.phone_number,indent)

        addr = candidate_resume_data.get('address',0)
        city = candidate_resume_data.get('city',0)
        state = candidate_resume_data.get('state',0)
        pincode = candidate_resume_data.get('pincode',0)
        claimed_skills= candidate_resume_data.get('claimed_skills',0)
        gender = candidate_resume_data.get('gender',0)
        dateofbirth= candidate_resume_data.get('dateofbirth',0)
        licenseno = candidate_resume_data.get('licenseno',0)
        summary = candidate_resume_data.get('summary',0)
        nationality = candidate_resume_data.get('nationality',0)

        indent_majority = ''
        for i in range(indent):
                indent_majority += '\t'

        # Mock the current address field from the parsed resume dictionary
        resp += indent_majority + '<currentAddress>\r\n'
        if addr:
                resp += _add_xml_field("address1",addr, indent+1)
        else:
                resp += _add_xml_field("address1","", indent+1)
        resp += _add_xml_field("address2","", indent+1)
        if city:
                resp += _add_xml_field("city", city, indent+1)
        else:
                resp += _add_xml_field("city", '', indent+1)
        if state:
                resp += _add_xml_field("state", state, indent+1)
        else:
                resp += _add_xml_field("state", '', indent+1)
        if pincode:
                resp += _add_xml_field("pinCode", pincode, indent+1)
        else:
                resp += _add_xml_field("pinCode", '', indent+1)
        resp += indent_majority + '</currentAddress>\r\n'

        # Permenant Address fields are always blank in the newProfile fields after the resume parser
        resp += indent_majority +'<permenantAddress>\r\n'
        addr_fields = _get_required_object_fields("address")
        (response, flag) = _add_fields(addr_fields, PermenantAddress(), indent+1, True)
        resp += response
        resp += indent_majority +'</permenantAddress>\r\n'
        # Build candidate profile response
        if gender:
                resp += _add_xml_field("gender", gender, indent)
        else:
                resp += indent_majority + '<gender/>\r\n'
        if dateofbirth:
                resp += _add_xml_field("birthdate", dateofbirth, indent)
        else:
                resp += indent_majority + '<birthdate/>\r\n'
        resp += indent_majority + '<dl_type/>\r\n'
        if licenseno:
                resp += _add_xml_field("dl_number", licenseno, indent)
        else:
                resp += indent_majority + '<dl_number/>\r\n'
        if nationality:
                resp += _add_xml_field("nationality", nationality, indent)
        else:
                resp += indent_majority + '<nationality/>\r\n'
        resp += indent_majority + '<dl_expiry/>\r\n'
        resp += indent_majority + '<height/>\r\n'
        resp += indent_majority + '<weight/>\r\n'
        resp += indent_majority + '<dl_expiry/>\r\n'
        resp += indent_majority + '<dl_registered_state/>\r\n'
        resp += indent_majority + '<interested_jobs/>\r\n'
        resp += indent_majority + '<dreamJob/>\r\n'
        resp += indent_majority + '<personalityStrengths/>\r\n'
        resp += indent_majority + '<personalityWeaknesses/>\r\n'
        resp += indent_majority + '<totalExperience/>\r\n'
        resp += indent_majority + '<annualCtc/>\r\n'
        resp += indent_majority + '<curSalary/>\r\n'
        resp += indent_majority + '<curSalaryFreq/>\r\n'
        resp += indent_majority + '<curSalaryCurrency/>\r\n'
        resp += indent_majority + '<expectedRaise/>\r\n'
        resp += indent_majority + '<expSalary/>\r\n'
        resp += indent_majority + '<expSalaryFreq/>\r\n'
        resp += indent_majority + '<expSalaryCurrency/>\r\n'
        resp += indent_majority + '<noticePeriod/>\r\n'
        resp += indent_majority + '<relocation/>\r\n'
                resp += indent_majority + '<linkedInProfile/>\r\n'
        resp += indent_majority + '<gitHubProfile/>\r\n'
        resp += indent_majority + '<queryHomeProfile/>\r\n'
        resp += _add_xml_field('status','Looking for job',indent)
        resp += indent_majority + '<reference/>\r\n'
        if summary:
                resp += _add_xml_field("summary",summary, indent)
        else:
                resp += indent_majority +'<summary/>\r\n'
        resp += indent_majority + '<Degree/>\r\n'
        resp += indent_majority + '<WorkExperience/>\r\n'
        resp += indent_majority + '<uniqueId/>\r\n'
        resp += _add_xml_field("ownTwoWheeler", False, indent)
        resp += '\t\t</newProfile>\r\n'
        return resp
#end of _response_builder_from_parser_resume_data
                                                                                              
def _inline_response_builder(resp,request,candidate,cand_resume_data,res_fn):
        cid=candidate.id
        _change_filename(cand_resume_data,cid)
        if not int(candidate.phone_number):
                for phone_field in ['phone','mobile','formattedphone','formattedmobile']:
                                if cand_resume_data.get(phone_field,0):
                                        candidate.phone_number=cand_resume_data[phone_field]
        if not candidate.user.last_name:
                if cand_resume_data.get('lastname',0):
                        candidate.user.last_name=cand_resume_data['lastname']
        candidate.save()
        resp +='<resume>\r\n'
        resp += _add_xml_field("filename", res_fn)
        resp += '\t<candidate>\r\n'
        existing_resp =_fetch_profile_helper(request,cid)
        if not existing_resp:
                resp += '\t\t<existingProfile/>\r\n'
                _update_parsed_candidate_profile_helper(cand_resume_data,candidate)
        else:
                resp += existing_resp
        response = _response_builder_from_parsed_resume_data(candidate,cand_resume_data,'')
        resp += response
        resp += '\t</candidate>\r\n'
        return resp

def _change_filename(cand_resume_data,cid):
        org_filename=cand_resume_data['rchillie_resp_file']
        mod_filename=cand_resume_data['rchillie_resp_file']=cand_resume_data['rchillie_resp_file'][:15]+'_%s.txt'%cid
        retval = call(['mv','/content/candidates/resume_responses/%s'%org_filename,'/content/candidates/resume_responses/%s'%mod_filename])
        if retval !=0:
                logr.info("resume response file is not getting saved")
        org_error_file = cand_resume_data['error_file']
        mod_error_file = cand_resume_data['error_file'] = org_error_file[:6]+'_%s.txt'%cid
        error_file_path = '/content/candidates/resume_responses/errors/%s'%org_error_file
        if os.path.exists(error_file_path):
                retval = call(['mv',error_file_path,'/content/candidates/resume_responses/errors/%s'%mod_error_file])
        if retval !=0:
                logr.info("resume error file is not getting saved")
#End of _change_filename()

# Upload resume helper function
def _upload_resume(request, candidate, is_tmp_stored = False):

        logr.info("Incoming request to upload resume; user: %s" % request.user.email)

        resp = ''
        errors = ''

        cont_len = request.META['CONTENT_LENGTH']
        if (int(cont_len) > 2048575):
                errors += 'Invalid value (%s) for the field %s'%(cont_len,"Content-Length header")
                resp += '<errors>\r\n'
                resp += _add_xml_field('errorStr',errors)
                resp += '</errors>\r\n'
                return resp

        # Read the request body
        header, data = request.body.split(',', 1)

        header = header[5:]     # Header starts with "data:", so skip first 5 bytes

        cont_type, encoding = header.split(';', 1)

        valid_content_types = {'application/pdf': 'pdf', 'application/msword': 'doc' , 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.template':'dotx', 'application/vnd.ms-word.document.macroEnabled.12':'docm', 'application/vnd.ms-word.template.macroEnabled.12':'dotm'}

        if cont_type not in valid_content_types.keys():
                errors += 'Invalid Content Type'
                resp += _add_xml_field('errors',errors)
                return resp
        else:
                # Fabricate our own resume file name - to avoid conflicts such as two people having file name as "resume.doc"
                res_fn = 'resume_%s.%s' % (candidate.id, valid_content_types[cont_type])

        if is_tmp_stored:
                path = '/tmp/%s' % res_fn
                try:
                        with open(path, 'wb+') as destination:
                                destination.write(b64decode(data.split('#')[0]))
                                resp += _add_xml_field("success", res_fn)
                        return resp
                except Exception as e:
                        logr.info('Exception: %s' % str(e))
                        errors += 'Error while saving the resume'
                        resp +='<errors>\r\n'
                        resp += _add_xml_field('errorStr',errors)
                        resp +='</errors>\r\n'
                        return resp
        else:
                path = '/content/candidates/resume/%s' % res_fn
                resumeUrl = "./images/content/s3content/candidates/resume/%s" % res_fn
                if _isJobSeeker(request.user):
                        parsed_data_set = ParsedResumeData.objects.filter(candidate_id = candidate.id).order_by('-create_time')
                        if len(parsed_data_set) > 0:
                                parsed_data = parsed_data_set[0]
                        else:
                                parsed_data = None
                        year_ago = timezone.now() - timedelta(days = 365)

                        if not parsed_data:
                                (cand_resume_data,error_resp) = _resume_parser(cont_type,data,'')
                                if error_resp != '':
                                        resp +='<resume>\r\n'
                                        resp += error_resp
                                        resp +='</resume>\r\n'
                                        return resp
                                else:
                                        resp += _inline_response_builder(resp,request,candidate,cand_resume_data,res_fn)
                        elif parsed_data.create_time < year_ago:
                                (cand_resume_data,error_resp) = _resume_parser(cont_type,data,'')
                                if error_resp != '':
                                        resp +='<resume>\r\n'
                                        resp += error_resp
                                        resp +='</resume>\r\n'
                                        return resp
                                else:
                                        resp += _inline_response_builder(resp,request,candidate,cand_resume_data,res_fn)
                        else:
                                resp +='<errors>\r\n'
                                resp += _add_xml_field('errorStr','Resume upload allowed only once per year')
                                resp += _add_xml_field('filename','%s'%candidate.resume_filename)
                                resp +='</errors>\r\n'
                                return resp

                # If there's an existing resume URL set in candidate object, delete the old file
                if candidate.resume_filename:
                        old_filename=candidate.resume_filename
                        old_path = '/content/candidates/resume/%s' % old_filename
                        try:
                                os.remove(old_path)
                        except Exception:
                                pass
                try:
                        with open(path, 'wb+') as destination:
                                destination.write(b64decode(data.split('#')[0]))
                                candidate.resume_filename = res_fn
                                candidate.save()
                                resp += _add_xml_field("success", res_fn)
                                if _isJobSeeker(request.user):
                                        resp +='</resume>\r\n'
                                return resp
                except Exception as e:
                        logr.info('Exception: %s' % str(e))
                        errors += 'Error while saving file'
                        resp += _add_xml_field('errors',errors)
                        if _isJobSeeker(request.user):
                                resp +='</resume>\r\n'
                        return resp
#End of _upload_resume()

def uploadResume(request):

        logr.info("Incoming request to upload resume; user: %s" % request.user.email)

        if request.method != 'POST':
                return HttpResponse(INVALID_METHOD, content_type="text/xml")

        candidate = Candidate.objects.get(user_id = request.user.id)
        resp = '<?xml version="1.0" encoding="UTF-8"?>\r\n'
        resp += _upload_resume(request,candidate)
        return HttpResponse(resp, content_type="text/xml")
#End of uploadResume
